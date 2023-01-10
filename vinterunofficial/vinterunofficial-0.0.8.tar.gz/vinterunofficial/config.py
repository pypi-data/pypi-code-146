from enum import Enum

APIBASE = "https://www.vinterapi.com/api/v3"

class Frequency(Enum):
    REAL_TIME = "r"
    HOURLY = "h"
    DAILY = "d"

class FrequencyApiType(Enum):
    REAL_TIME = "real_time"
    HOURLY = "hourly"
    DAILY = "daily"

class AssetType(Enum):
    MULTI_ASSET = "multi_assets"
    SINGLE_ASSET = "single_assets"

class ActiveAssetType(Enum):
    MULTI_ASSET = "active_multi_assets"
    SINGLE_ASSET = "active_single_assets"

class AssetUrl(Enum):
    MULTI_ASSET_REAL_TIME = {
        "frequency": Frequency.REAL_TIME,
        "asset_type": AssetType.MULTI_ASSET,
        "url": f"{APIBASE}/{AssetType.MULTI_ASSET.value}_{FrequencyApiType.REAL_TIME.value}",
    }
    SINGLE_ASSET_REAL_TIME = {
        "frequency": Frequency.REAL_TIME,
        "asset_type": AssetType.SINGLE_ASSET,
        "url": f"{APIBASE}/{AssetType.SINGLE_ASSET.value}_{FrequencyApiType.REAL_TIME.value}",
    }
    MULTI_ASSET_HOURLY = {
        "frequency": Frequency.HOURLY,
        "asset_type": AssetType.MULTI_ASSET,
        "url": f"{APIBASE}/{AssetType.MULTI_ASSET.value}_{FrequencyApiType.HOURLY.value}",
    }
    SINGLE_ASSET_HOURLY = {
        "frequency": Frequency.HOURLY,
        "asset_type": AssetType.SINGLE_ASSET,
        "url": f"{APIBASE}/{AssetType.SINGLE_ASSET.value}_{FrequencyApiType.HOURLY.value}",
    }
    MULTI_ASSET_DAILY = {
        "frequency": Frequency.DAILY,
        "asset_type": AssetType.MULTI_ASSET,
        "url": f"{APIBASE}/{AssetType.MULTI_ASSET.value}_{FrequencyApiType.DAILY.value}",
    }
    SINGLE_ASSET_DAILY = {
        "frequency": Frequency.DAILY,
        "asset_type": AssetType.SINGLE_ASSET,
        "url": f"{APIBASE}/{AssetType.SINGLE_ASSET.value}_{FrequencyApiType.DAILY.value}",
    }
    ACTIVE_MULTI_ASSET = {
        "frequency": None,
        "asset_type": AssetType.MULTI_ASSET,
        "url": f"{APIBASE}/{ActiveAssetType.MULTI_ASSET.value}",
    }
    ACTIVE_SINGLE_ASSET = {
        "frequency": None,
        "asset_type": AssetType.SINGLE_ASSET,
        "url": f"{APIBASE}/{ActiveAssetType.SINGLE_ASSET.value}",
    }