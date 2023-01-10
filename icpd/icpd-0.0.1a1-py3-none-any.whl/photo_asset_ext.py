import os
from typing import Any, Dict

from icloudpy.services.photos import PhotoAsset

from icpd import constants


class PhotoAssetExt(PhotoAsset):
    # # https://github.com/picklepete/pyicloud/pull/347
    # PHOTO_VERSION_LOOKUP = {
    #     "full": "resJPEGFull",
    #     "large": "resJPEGLarge",
    #     "medium": "resJPEGMed",
    #     "thumb": "resJPEGThumb",
    #     "sidecar": "resSidecar",
    #     "original": "resOriginal",
    #     "original_alt": "resOriginalAlt",
    # }

    # VIDEO_VERSION_LOOKUP = {
    #     "full": "resVidFull",
    #     "medium": "resVidMed",
    #     "thumb": "resVidSmall",
    #     "original": "resOriginal",
    #     "original_compl": "resOriginalVidCompl",
    # }
    FILETYPE_EXTENSIONS = {
        "com.apple.quicktime-movie": "MOV",
        "public.heic": "HEIC",
        "public.jpeg": "JPG",
        "public.png": "PNG",
        "public.mpeg-4": "MP4",
    }

    def __init__(self, photo: PhotoAsset):
        super().__init__(photo._service, photo._master_record, photo._asset_record)

        asset_basename, asset_fileext = os.path.splitext(self.filename)

        # asset_record contains download links to edited versions;
        # master_record contains links to originals.
        self._versions: Dict[str, Any] = {}
        prefix: str = "res"
        suffix: str = "Res"
        # for record in (self._asset_record, self._master_record):
        for record in (self._master_record, self._asset_record):
            record_type: str = record["recordType"]
            fields: Dict[str, Any] = record["fields"]
            for k, v in fields.items():
                if k.startswith(prefix) and k.endswith(suffix):
                    v_name: str = k[: -len(suffix)]
                    v_meta: Dict[str, Any] = v["value"]

                    v_file_type = fields.get(v_name + "FileType", {})["value"]
                    v_file_ext = self.FILETYPE_EXTENSIONS.get(
                        v_file_type, asset_fileext
                    )

                    this_version: Dict[str, Any] = {
                        "filename": asset_basename
                        + (
                            ""
                            if record_type == constants.MASTER_RECORD_TYPE
                            else "-edit"
                        )
                        + "."
                        + v_file_ext.lstrip("."),
                        "size": int(v_meta["size"]),
                        "url": v_meta["downloadURL"],
                        "width": int(fields.get(v_name + "Width", {})["value"]),
                        "height": int(fields.get(v_name + "Height", {})["value"]),
                        "type": v_file_type,
                        "source": record_type,
                    }

                    if k in self._versions and self._versions[k] != this_version:
                        self._versions[f"{k}-edit"] = this_version
                    else:
                        self._versions[k] = this_version

        self._is_favorite: bool = bool(
            int(self._asset_record["fields"].get("isFavorite", {}).get("value", 0))
        )
        self._is_hidden: bool = bool(
            int(self._asset_record["fields"].get("isHidden", {}).get("value", 0))
        )

        self._is_edited: bool = (
            constants.EDITED_PHOTO in self._versions
            or constants.EDITED_VIDEO in self._versions
        )

        # these are mutually exclusive:
        self._is_live: bool = (
            constants.ORIGINAL_MEDIA in self._versions
            and constants.ORIGINAL_LIVE in self._versions
        )
        self._is_video: bool = (
            not self._is_live and constants.MEDIUM_VIDEO in self._versions
        )  # stills don't have MEDIUM_VIDEO
        self._is_still: bool = not self._is_live and not self._is_video

        self._media_type: str = (
            "live"
            if self._is_live
            else "video"
            if self._is_video
            else "still"
            if self._is_still
            else "unknown"
        )

        self._largest_versions: Dict[str, Any] = {}
        _largest_versions_lkp: Dict[str, int] = {}
        for k, v in self._versions.items():
            v_file_name: str = v["filename"]
            v_file_size: int = v["size"]
            if v_file_size > _largest_versions_lkp.get(v_file_name, 0):
                _largest_versions_lkp[v_file_name] = v_file_size
                self._largest_versions[v_file_name] = {k: v}
        self._largest_versions = {
            k2: v2 for k, v in self._largest_versions.items() for k2, v2 in v.items()
        }

    @property
    def versions(self) -> dict:
        return self._versions

    @property
    def largest_versions(self) -> dict:
        return self._largest_versions

    @property
    def is_favorite(self) -> bool:
        return self._is_favorite

    @property
    def is_hidden(self) -> bool:
        return self._is_hidden

    @property
    def is_edited(self) -> bool:
        return self._is_edited

    @property
    def is_live(self) -> bool:
        return self._is_live

    @property
    def is_still(self) -> bool:
        return self._is_still

    @property
    def is_video(self) -> bool:
        return self._is_video

    @property
    def media_type(self) -> str:
        return self._media_type
