'''
# `cloudflare_zone_cache_variants`

Refer to the Terraform Registory for docs: [`cloudflare_zone_cache_variants`](https://www.terraform.io/docs/providers/cloudflare/r/zone_cache_variants).
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

import cdktf as _cdktf_9a9027ec
import constructs as _constructs_77d1e7e8


class ZoneCacheVariants(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-cloudflare.zoneCacheVariants.ZoneCacheVariants",
):
    '''Represents a {@link https://www.terraform.io/docs/providers/cloudflare/r/zone_cache_variants cloudflare_zone_cache_variants}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        zone_id: builtins.str,
        avif: typing.Optional[typing.Sequence[builtins.str]] = None,
        bmp: typing.Optional[typing.Sequence[builtins.str]] = None,
        gif: typing.Optional[typing.Sequence[builtins.str]] = None,
        id: typing.Optional[builtins.str] = None,
        jp2: typing.Optional[typing.Sequence[builtins.str]] = None,
        jpeg: typing.Optional[typing.Sequence[builtins.str]] = None,
        jpg: typing.Optional[typing.Sequence[builtins.str]] = None,
        jpg2: typing.Optional[typing.Sequence[builtins.str]] = None,
        png: typing.Optional[typing.Sequence[builtins.str]] = None,
        tif: typing.Optional[typing.Sequence[builtins.str]] = None,
        tiff: typing.Optional[typing.Sequence[builtins.str]] = None,
        webp: typing.Optional[typing.Sequence[builtins.str]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[jsii.Number] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://www.terraform.io/docs/providers/cloudflare/r/zone_cache_variants cloudflare_zone_cache_variants} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param zone_id: The zone identifier to target for the resource. **Modifying this attribute will force creation of a new resource.**. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/zone_cache_variants#zone_id ZoneCacheVariants#zone_id}
        :param avif: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/zone_cache_variants#avif ZoneCacheVariants#avif}.
        :param bmp: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/zone_cache_variants#bmp ZoneCacheVariants#bmp}.
        :param gif: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/zone_cache_variants#gif ZoneCacheVariants#gif}.
        :param id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/zone_cache_variants#id ZoneCacheVariants#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param jp2: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/zone_cache_variants#jp2 ZoneCacheVariants#jp2}.
        :param jpeg: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/zone_cache_variants#jpeg ZoneCacheVariants#jpeg}.
        :param jpg: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/zone_cache_variants#jpg ZoneCacheVariants#jpg}.
        :param jpg2: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/zone_cache_variants#jpg2 ZoneCacheVariants#jpg2}.
        :param png: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/zone_cache_variants#png ZoneCacheVariants#png}.
        :param tif: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/zone_cache_variants#tif ZoneCacheVariants#tif}.
        :param tiff: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/zone_cache_variants#tiff ZoneCacheVariants#tiff}.
        :param webp: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/zone_cache_variants#webp ZoneCacheVariants#webp}.
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6182c0f5085287c30b04cfcc97155c89b372750ee22d9009b7669a3e95c3e960)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = ZoneCacheVariantsConfig(
            zone_id=zone_id,
            avif=avif,
            bmp=bmp,
            gif=gif,
            id=id,
            jp2=jp2,
            jpeg=jpeg,
            jpg=jpg,
            jpg2=jpg2,
            png=png,
            tif=tif,
            tiff=tiff,
            webp=webp,
            connection=connection,
            count=count,
            depends_on=depends_on,
            for_each=for_each,
            lifecycle=lifecycle,
            provider=provider,
            provisioners=provisioners,
        )

        jsii.create(self.__class__, self, [scope, id_, config])

    @jsii.member(jsii_name="resetAvif")
    def reset_avif(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAvif", []))

    @jsii.member(jsii_name="resetBmp")
    def reset_bmp(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBmp", []))

    @jsii.member(jsii_name="resetGif")
    def reset_gif(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetGif", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetJp2")
    def reset_jp2(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetJp2", []))

    @jsii.member(jsii_name="resetJpeg")
    def reset_jpeg(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetJpeg", []))

    @jsii.member(jsii_name="resetJpg")
    def reset_jpg(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetJpg", []))

    @jsii.member(jsii_name="resetJpg2")
    def reset_jpg2(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetJpg2", []))

    @jsii.member(jsii_name="resetPng")
    def reset_png(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPng", []))

    @jsii.member(jsii_name="resetTif")
    def reset_tif(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTif", []))

    @jsii.member(jsii_name="resetTiff")
    def reset_tiff(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTiff", []))

    @jsii.member(jsii_name="resetWebp")
    def reset_webp(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetWebp", []))

    @jsii.member(jsii_name="synthesizeAttributes")
    def _synthesize_attributes(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "synthesizeAttributes", []))

    @jsii.python.classproperty
    @jsii.member(jsii_name="tfResourceType")
    def TF_RESOURCE_TYPE(cls) -> builtins.str:
        return typing.cast(builtins.str, jsii.sget(cls, "tfResourceType"))

    @builtins.property
    @jsii.member(jsii_name="avifInput")
    def avif_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "avifInput"))

    @builtins.property
    @jsii.member(jsii_name="bmpInput")
    def bmp_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "bmpInput"))

    @builtins.property
    @jsii.member(jsii_name="gifInput")
    def gif_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "gifInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="jp2Input")
    def jp2_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "jp2Input"))

    @builtins.property
    @jsii.member(jsii_name="jpegInput")
    def jpeg_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "jpegInput"))

    @builtins.property
    @jsii.member(jsii_name="jpg2Input")
    def jpg2_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "jpg2Input"))

    @builtins.property
    @jsii.member(jsii_name="jpgInput")
    def jpg_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "jpgInput"))

    @builtins.property
    @jsii.member(jsii_name="pngInput")
    def png_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "pngInput"))

    @builtins.property
    @jsii.member(jsii_name="tiffInput")
    def tiff_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "tiffInput"))

    @builtins.property
    @jsii.member(jsii_name="tifInput")
    def tif_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "tifInput"))

    @builtins.property
    @jsii.member(jsii_name="webpInput")
    def webp_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "webpInput"))

    @builtins.property
    @jsii.member(jsii_name="zoneIdInput")
    def zone_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "zoneIdInput"))

    @builtins.property
    @jsii.member(jsii_name="avif")
    def avif(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "avif"))

    @avif.setter
    def avif(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__33ce883b7b62cbdc46871f8b5efbaf53bc987fb9987a8f3e9988daba80a9e159)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "avif", value)

    @builtins.property
    @jsii.member(jsii_name="bmp")
    def bmp(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "bmp"))

    @bmp.setter
    def bmp(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dbf08a35b52e99d3b00a6c9a8b87ba9f395a223ed0bd53000602dd78ba809674)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "bmp", value)

    @builtins.property
    @jsii.member(jsii_name="gif")
    def gif(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "gif"))

    @gif.setter
    def gif(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__58f0f7e459375f42e0f4fa0fffbd9feb76b86bf285dca2f1142e16df020a0f13)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "gif", value)

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__381ec3266edc0e785af11e8b50821b0f7b630145bf8a91b6e5e3be98a904d09c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value)

    @builtins.property
    @jsii.member(jsii_name="jp2")
    def jp2(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "jp2"))

    @jp2.setter
    def jp2(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8abf3508da2d77d4f87a07d6c0ce47afe0a9405ea510e0ec7fad10739ec7f62a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "jp2", value)

    @builtins.property
    @jsii.member(jsii_name="jpeg")
    def jpeg(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "jpeg"))

    @jpeg.setter
    def jpeg(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__91d2eb7218970f506b802093942ce7642e46949cb61f03de712753af14de6528)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "jpeg", value)

    @builtins.property
    @jsii.member(jsii_name="jpg")
    def jpg(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "jpg"))

    @jpg.setter
    def jpg(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__244019c373e81569951429272ade329f7922b85c9803efb79a62afa49fc70104)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "jpg", value)

    @builtins.property
    @jsii.member(jsii_name="jpg2")
    def jpg2(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "jpg2"))

    @jpg2.setter
    def jpg2(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__186454d214fe6de8977073945e5665ce5d5d7e5075d742481c2968118619f5ce)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "jpg2", value)

    @builtins.property
    @jsii.member(jsii_name="png")
    def png(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "png"))

    @png.setter
    def png(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7f3e62b34b8dea18f1503489773df1ae7e9ad1c079065c2bbafd47abb0fffec3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "png", value)

    @builtins.property
    @jsii.member(jsii_name="tif")
    def tif(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "tif"))

    @tif.setter
    def tif(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e8fba17b7c81c44d91a54020c0c24c67b6a0eb4d234152e5008fefbd75411916)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tif", value)

    @builtins.property
    @jsii.member(jsii_name="tiff")
    def tiff(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "tiff"))

    @tiff.setter
    def tiff(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6d06012772f60b2c849d36db7f9233d5762d501278209df9068a73c8f99c9d4e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tiff", value)

    @builtins.property
    @jsii.member(jsii_name="webp")
    def webp(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "webp"))

    @webp.setter
    def webp(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8101c9dcf5bb1f718a0a4c1851fcc3f021b72f616b0443a0300838108acdc3ef)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "webp", value)

    @builtins.property
    @jsii.member(jsii_name="zoneId")
    def zone_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "zoneId"))

    @zone_id.setter
    def zone_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7b7119257035a242880c47b1f6f5d7f0edb1b3cf0be52ef5baf37383806ead6e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "zoneId", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-cloudflare.zoneCacheVariants.ZoneCacheVariantsConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "zone_id": "zoneId",
        "avif": "avif",
        "bmp": "bmp",
        "gif": "gif",
        "id": "id",
        "jp2": "jp2",
        "jpeg": "jpeg",
        "jpg": "jpg",
        "jpg2": "jpg2",
        "png": "png",
        "tif": "tif",
        "tiff": "tiff",
        "webp": "webp",
    },
)
class ZoneCacheVariantsConfig(_cdktf_9a9027ec.TerraformMetaArguments):
    def __init__(
        self,
        *,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[jsii.Number] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
        zone_id: builtins.str,
        avif: typing.Optional[typing.Sequence[builtins.str]] = None,
        bmp: typing.Optional[typing.Sequence[builtins.str]] = None,
        gif: typing.Optional[typing.Sequence[builtins.str]] = None,
        id: typing.Optional[builtins.str] = None,
        jp2: typing.Optional[typing.Sequence[builtins.str]] = None,
        jpeg: typing.Optional[typing.Sequence[builtins.str]] = None,
        jpg: typing.Optional[typing.Sequence[builtins.str]] = None,
        jpg2: typing.Optional[typing.Sequence[builtins.str]] = None,
        png: typing.Optional[typing.Sequence[builtins.str]] = None,
        tif: typing.Optional[typing.Sequence[builtins.str]] = None,
        tiff: typing.Optional[typing.Sequence[builtins.str]] = None,
        webp: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param zone_id: The zone identifier to target for the resource. **Modifying this attribute will force creation of a new resource.**. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/zone_cache_variants#zone_id ZoneCacheVariants#zone_id}
        :param avif: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/zone_cache_variants#avif ZoneCacheVariants#avif}.
        :param bmp: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/zone_cache_variants#bmp ZoneCacheVariants#bmp}.
        :param gif: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/zone_cache_variants#gif ZoneCacheVariants#gif}.
        :param id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/zone_cache_variants#id ZoneCacheVariants#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param jp2: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/zone_cache_variants#jp2 ZoneCacheVariants#jp2}.
        :param jpeg: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/zone_cache_variants#jpeg ZoneCacheVariants#jpeg}.
        :param jpg: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/zone_cache_variants#jpg ZoneCacheVariants#jpg}.
        :param jpg2: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/zone_cache_variants#jpg2 ZoneCacheVariants#jpg2}.
        :param png: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/zone_cache_variants#png ZoneCacheVariants#png}.
        :param tif: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/zone_cache_variants#tif ZoneCacheVariants#tif}.
        :param tiff: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/zone_cache_variants#tiff ZoneCacheVariants#tiff}.
        :param webp: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/zone_cache_variants#webp ZoneCacheVariants#webp}.
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0ecb5647116c380ffb859538a69ac283a47c20e45b6455ca8798f72eb53fde79)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument zone_id", value=zone_id, expected_type=type_hints["zone_id"])
            check_type(argname="argument avif", value=avif, expected_type=type_hints["avif"])
            check_type(argname="argument bmp", value=bmp, expected_type=type_hints["bmp"])
            check_type(argname="argument gif", value=gif, expected_type=type_hints["gif"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument jp2", value=jp2, expected_type=type_hints["jp2"])
            check_type(argname="argument jpeg", value=jpeg, expected_type=type_hints["jpeg"])
            check_type(argname="argument jpg", value=jpg, expected_type=type_hints["jpg"])
            check_type(argname="argument jpg2", value=jpg2, expected_type=type_hints["jpg2"])
            check_type(argname="argument png", value=png, expected_type=type_hints["png"])
            check_type(argname="argument tif", value=tif, expected_type=type_hints["tif"])
            check_type(argname="argument tiff", value=tiff, expected_type=type_hints["tiff"])
            check_type(argname="argument webp", value=webp, expected_type=type_hints["webp"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "zone_id": zone_id,
        }
        if connection is not None:
            self._values["connection"] = connection
        if count is not None:
            self._values["count"] = count
        if depends_on is not None:
            self._values["depends_on"] = depends_on
        if for_each is not None:
            self._values["for_each"] = for_each
        if lifecycle is not None:
            self._values["lifecycle"] = lifecycle
        if provider is not None:
            self._values["provider"] = provider
        if provisioners is not None:
            self._values["provisioners"] = provisioners
        if avif is not None:
            self._values["avif"] = avif
        if bmp is not None:
            self._values["bmp"] = bmp
        if gif is not None:
            self._values["gif"] = gif
        if id is not None:
            self._values["id"] = id
        if jp2 is not None:
            self._values["jp2"] = jp2
        if jpeg is not None:
            self._values["jpeg"] = jpeg
        if jpg is not None:
            self._values["jpg"] = jpg
        if jpg2 is not None:
            self._values["jpg2"] = jpg2
        if png is not None:
            self._values["png"] = png
        if tif is not None:
            self._values["tif"] = tif
        if tiff is not None:
            self._values["tiff"] = tiff
        if webp is not None:
            self._values["webp"] = webp

    @builtins.property
    def connection(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, _cdktf_9a9027ec.WinrmProvisionerConnection]]:
        '''
        :stability: experimental
        '''
        result = self._values.get("connection")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, _cdktf_9a9027ec.WinrmProvisionerConnection]], result)

    @builtins.property
    def count(self) -> typing.Optional[jsii.Number]:
        '''
        :stability: experimental
        '''
        result = self._values.get("count")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def depends_on(
        self,
    ) -> typing.Optional[typing.List[_cdktf_9a9027ec.ITerraformDependable]]:
        '''
        :stability: experimental
        '''
        result = self._values.get("depends_on")
        return typing.cast(typing.Optional[typing.List[_cdktf_9a9027ec.ITerraformDependable]], result)

    @builtins.property
    def for_each(self) -> typing.Optional[_cdktf_9a9027ec.ITerraformIterator]:
        '''
        :stability: experimental
        '''
        result = self._values.get("for_each")
        return typing.cast(typing.Optional[_cdktf_9a9027ec.ITerraformIterator], result)

    @builtins.property
    def lifecycle(self) -> typing.Optional[_cdktf_9a9027ec.TerraformResourceLifecycle]:
        '''
        :stability: experimental
        '''
        result = self._values.get("lifecycle")
        return typing.cast(typing.Optional[_cdktf_9a9027ec.TerraformResourceLifecycle], result)

    @builtins.property
    def provider(self) -> typing.Optional[_cdktf_9a9027ec.TerraformProvider]:
        '''
        :stability: experimental
        '''
        result = self._values.get("provider")
        return typing.cast(typing.Optional[_cdktf_9a9027ec.TerraformProvider], result)

    @builtins.property
    def provisioners(
        self,
    ) -> typing.Optional[typing.List[typing.Union[_cdktf_9a9027ec.FileProvisioner, _cdktf_9a9027ec.LocalExecProvisioner, _cdktf_9a9027ec.RemoteExecProvisioner]]]:
        '''
        :stability: experimental
        '''
        result = self._values.get("provisioners")
        return typing.cast(typing.Optional[typing.List[typing.Union[_cdktf_9a9027ec.FileProvisioner, _cdktf_9a9027ec.LocalExecProvisioner, _cdktf_9a9027ec.RemoteExecProvisioner]]], result)

    @builtins.property
    def zone_id(self) -> builtins.str:
        '''The zone identifier to target for the resource. **Modifying this attribute will force creation of a new resource.**.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/zone_cache_variants#zone_id ZoneCacheVariants#zone_id}
        '''
        result = self._values.get("zone_id")
        assert result is not None, "Required property 'zone_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def avif(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/zone_cache_variants#avif ZoneCacheVariants#avif}.'''
        result = self._values.get("avif")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def bmp(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/zone_cache_variants#bmp ZoneCacheVariants#bmp}.'''
        result = self._values.get("bmp")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def gif(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/zone_cache_variants#gif ZoneCacheVariants#gif}.'''
        result = self._values.get("gif")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/zone_cache_variants#id ZoneCacheVariants#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def jp2(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/zone_cache_variants#jp2 ZoneCacheVariants#jp2}.'''
        result = self._values.get("jp2")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def jpeg(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/zone_cache_variants#jpeg ZoneCacheVariants#jpeg}.'''
        result = self._values.get("jpeg")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def jpg(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/zone_cache_variants#jpg ZoneCacheVariants#jpg}.'''
        result = self._values.get("jpg")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def jpg2(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/zone_cache_variants#jpg2 ZoneCacheVariants#jpg2}.'''
        result = self._values.get("jpg2")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def png(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/zone_cache_variants#png ZoneCacheVariants#png}.'''
        result = self._values.get("png")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def tif(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/zone_cache_variants#tif ZoneCacheVariants#tif}.'''
        result = self._values.get("tif")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def tiff(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/zone_cache_variants#tiff ZoneCacheVariants#tiff}.'''
        result = self._values.get("tiff")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def webp(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/zone_cache_variants#webp ZoneCacheVariants#webp}.'''
        result = self._values.get("webp")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ZoneCacheVariantsConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "ZoneCacheVariants",
    "ZoneCacheVariantsConfig",
]

publication.publish()

def _typecheckingstub__6182c0f5085287c30b04cfcc97155c89b372750ee22d9009b7669a3e95c3e960(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    zone_id: builtins.str,
    avif: typing.Optional[typing.Sequence[builtins.str]] = None,
    bmp: typing.Optional[typing.Sequence[builtins.str]] = None,
    gif: typing.Optional[typing.Sequence[builtins.str]] = None,
    id: typing.Optional[builtins.str] = None,
    jp2: typing.Optional[typing.Sequence[builtins.str]] = None,
    jpeg: typing.Optional[typing.Sequence[builtins.str]] = None,
    jpg: typing.Optional[typing.Sequence[builtins.str]] = None,
    jpg2: typing.Optional[typing.Sequence[builtins.str]] = None,
    png: typing.Optional[typing.Sequence[builtins.str]] = None,
    tif: typing.Optional[typing.Sequence[builtins.str]] = None,
    tiff: typing.Optional[typing.Sequence[builtins.str]] = None,
    webp: typing.Optional[typing.Sequence[builtins.str]] = None,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[jsii.Number] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__33ce883b7b62cbdc46871f8b5efbaf53bc987fb9987a8f3e9988daba80a9e159(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dbf08a35b52e99d3b00a6c9a8b87ba9f395a223ed0bd53000602dd78ba809674(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__58f0f7e459375f42e0f4fa0fffbd9feb76b86bf285dca2f1142e16df020a0f13(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__381ec3266edc0e785af11e8b50821b0f7b630145bf8a91b6e5e3be98a904d09c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8abf3508da2d77d4f87a07d6c0ce47afe0a9405ea510e0ec7fad10739ec7f62a(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__91d2eb7218970f506b802093942ce7642e46949cb61f03de712753af14de6528(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__244019c373e81569951429272ade329f7922b85c9803efb79a62afa49fc70104(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__186454d214fe6de8977073945e5665ce5d5d7e5075d742481c2968118619f5ce(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7f3e62b34b8dea18f1503489773df1ae7e9ad1c079065c2bbafd47abb0fffec3(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e8fba17b7c81c44d91a54020c0c24c67b6a0eb4d234152e5008fefbd75411916(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6d06012772f60b2c849d36db7f9233d5762d501278209df9068a73c8f99c9d4e(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8101c9dcf5bb1f718a0a4c1851fcc3f021b72f616b0443a0300838108acdc3ef(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7b7119257035a242880c47b1f6f5d7f0edb1b3cf0be52ef5baf37383806ead6e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0ecb5647116c380ffb859538a69ac283a47c20e45b6455ca8798f72eb53fde79(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[jsii.Number] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    zone_id: builtins.str,
    avif: typing.Optional[typing.Sequence[builtins.str]] = None,
    bmp: typing.Optional[typing.Sequence[builtins.str]] = None,
    gif: typing.Optional[typing.Sequence[builtins.str]] = None,
    id: typing.Optional[builtins.str] = None,
    jp2: typing.Optional[typing.Sequence[builtins.str]] = None,
    jpeg: typing.Optional[typing.Sequence[builtins.str]] = None,
    jpg: typing.Optional[typing.Sequence[builtins.str]] = None,
    jpg2: typing.Optional[typing.Sequence[builtins.str]] = None,
    png: typing.Optional[typing.Sequence[builtins.str]] = None,
    tif: typing.Optional[typing.Sequence[builtins.str]] = None,
    tiff: typing.Optional[typing.Sequence[builtins.str]] = None,
    webp: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass
