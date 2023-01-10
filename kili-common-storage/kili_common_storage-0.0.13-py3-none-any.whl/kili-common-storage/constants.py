RESOURCE_SYS = "sys"
RESOURCE_GOODS_IMAGE = "goods-image"
RESOURCE_GOODS_VIDEO = "goods-video"
RESOURCE_SELLER_INFO = "seller-info"
RESOURCE_STORE_INFO = "store-info"
RESOURCE_SELECTIVE_IMAGES = "selective-images"
RESOURCE_BIG_DISCOUNT_SALE_TAG = "big-discount-sale-tag"
RESOURCE_TOP_SALES_EXCEL = "top-sales-excel"
RESOURCE_SAGAWA_LABEL = "sagawa-label"
RESOURCE_SEARCH_RECORDS_EXPORT = "search-records-export"
RESOURCE_BRAND = "brand"
RESOURCE_CLEARING = "clearing"
RESOURCE_CLEARING_STATISTICS = "clearing-statistics"
RESOURCE_MONTHLY_CLEARING_DNX = "monthly-clearing-dnx"
RESOURCE_BANNER = "banner"
RESOURCE_AFTER_SALE = "after-sale"
RESOURCE_REVIEW_IMAGE = "review-image"
RESOURCE_REVIEW_VIDEO = "review-video"
RESOURCE_COUNTRY_FLAGS = "country-flags"
RESOURCE_TOPIC_PAGE = "topic-page"
RESOURCE_SKIN = "skin"
RESOURCE_SALES_ORDER_EXCEL = "sales-order-excel"
RESOURCE_PACKAGE_EXCEL = "package-excel"
RESOURCE_GOODS_PENDING_DISPATCH_EXCEL = "goods-pending-dispatch-excel"
RESOURCE_REFUND_SLIP_EXCEL = "refund-slip-excel"
RESOURCE_IMAGE_SEARCH = "image-search"
RESOURCE_AVATAR = "avatar"
RESOURCE_GOODS_EXPORT = "goods-export"
RESOURCE_CATEGORY = "category"
RESOURCE_APP_SHORTCUT_ICON = "app-shortcut-icon"
RESOURCE_ADS_IMAGE = "ads-image"
RESOURCE_SPLASH_IMAGE = "splash-image"
RESOURCE_COMMISSION = "commission"
RESOURCE_FILE_CACHE = "file-cache"

# 正式文件路径映射
OBJECT_STORAGE_PATHS = {
    RESOURCE_SYS: "{prefix}/common/sys",
    RESOURCE_GOODS_IMAGE: "{prefix}/public/store/{store}/goods/image",
    RESOURCE_GOODS_VIDEO: "{prefix}/public/store/{store}/goods/video",
    RESOURCE_SELLER_INFO: "{prefix}/public/seller-info",
    RESOURCE_STORE_INFO: "{prefix}/public/store-info",
    RESOURCE_SELECTIVE_IMAGES: "{prefix}/public/selective-image",
    RESOURCE_BIG_DISCOUNT_SALE_TAG: "{prefix}/public/big-discount",
    RESOURCE_TOP_SALES_EXCEL: "{prefix}/public/top-sales-excel",
    RESOURCE_SAGAWA_LABEL: "{prefix}/public/sagawa-label",
    RESOURCE_SEARCH_RECORDS_EXPORT: "{prefix}/public/search-records-export",
    RESOURCE_BRAND: "{prefix}/public/brand-image",
    RESOURCE_CLEARING: "{prefix}/public/clearing",
    RESOURCE_CLEARING_STATISTICS: "{prefix}/public/clearing-statistics",
    RESOURCE_MONTHLY_CLEARING_DNX: "{prefix}/public/monthly-clearing-dnx",
    RESOURCE_BANNER: "{prefix}/public/banner-image",
    RESOURCE_AFTER_SALE: "{prefix}/public/user/after-sale",
    RESOURCE_REVIEW_IMAGE: "{prefix}/public/user/review/image", 
    RESOURCE_REVIEW_VIDEO: "{prefix}/public/user/review/video",
    RESOURCE_COUNTRY_FLAGS: "{prefix}/common/country-flags",
    RESOURCE_TOPIC_PAGE: "{prefix}/public/topic-page-image",
    RESOURCE_SKIN: "{prefix}/public/skin",
    RESOURCE_SALES_ORDER_EXCEL: "{prefix}/public/sales-order-excel",
    RESOURCE_PACKAGE_EXCEL: "{prefix}/public/package-excel",
    RESOURCE_GOODS_PENDING_DISPATCH_EXCEL: "{prefix}/public/goods-pending-dispatch-excel",
    RESOURCE_REFUND_SLIP_EXCEL: "{prefix}/public/refund-slip-excel",
    RESOURCE_IMAGE_SEARCH: "{prefix}/public/user/image-search",
    RESOURCE_AVATAR: "{prefix}/public/user/{user}/avatar",
    RESOURCE_GOODS_EXPORT: "{prefix}/public/goods-export",
    RESOURCE_CATEGORY: "{prefix}/common/category-icon",
    RESOURCE_APP_SHORTCUT_ICON: "{prefix}/common/app-shortcut-icon",
    RESOURCE_ADS_IMAGE: "{prefix}/common/ads-image",
    RESOURCE_SPLASH_IMAGE: "{prefix}/common/splash-image",
    RESOURCE_COMMISSION: "{prefix}/common/commission",
    RESOURCE_FILE_CACHE: "{prefix}/file-cache/{region}"
}

# 临时文件路径映射
OBJECT_STORAGE_PATHS_TEMP = {
    RESOURCE_GOODS_IMAGE: "{prefix}/public-temp/store/{store}/goods/image",
    RESOURCE_GOODS_VIDEO: "{prefix}/public-temp/store/{store}/goods/video",
    RESOURCE_SELLER_INFO: "{prefix}/public-temp/seller-info",
    RESOURCE_STORE_INFO: "{prefix}/public-temp/store-info",
    RESOURCE_SELECTIVE_IMAGES: "{prefix}/public-temp/selective-image",
    RESOURCE_BIG_DISCOUNT_SALE_TAG: "{prefix}/public-temp/big-discount",
    RESOURCE_SEARCH_RECORDS_EXPORT: "{prefix}/public-temp/search-records-export",
    RESOURCE_BRAND: "{prefix}/public-temp/brand-image",
    RESOURCE_BANNER: "{prefix}/public-temp/banner-image",
    RESOURCE_AFTER_SALE: "{prefix}/public-temp/user/after-sale",
    RESOURCE_REVIEW_IMAGE: "{prefix}/public-temp/user/review/image",
    RESOURCE_REVIEW_VIDEO: "{prefix}/public-temp/user/review/video",
    RESOURCE_COUNTRY_FLAGS: "{prefix}/common-temp/country-flags",
    RESOURCE_CATEGORY: "{prefix}/common-temp/category-icon",
    RESOURCE_APP_SHORTCUT_ICON: "{prefix}/common-temp/app-shortcut-icon",
    RESOURCE_COMMISSION: "{prefix}/common-temp/commission"
}

# 允许的文件类型
OBJECT_STORAGE_FILE_FORMAT_WHITELIST = {
    RESOURCE_SYS: ['jpg', 'png', 'jpeg', 'gif'],
    RESOURCE_GOODS_IMAGE: ['jpg', 'png', 'jpeg', 'gif'],
    RESOURCE_GOODS_VIDEO: ['mp4'],
    RESOURCE_SELLER_INFO: ['jpg', 'png', 'jpeg', 'gif'],
    RESOURCE_STORE_INFO: ['jpg', 'png', 'jpeg', 'gif'],
    RESOURCE_SELECTIVE_IMAGES: ['jpg', 'png', 'jpeg', 'gif'],
    RESOURCE_BIG_DISCOUNT_SALE_TAG: ['jpg', 'png', 'jpeg', 'gif'],
    RESOURCE_TOP_SALES_EXCEL: ['xlsx', 'xls'],
    RESOURCE_SAGAWA_LABEL: ['pdf'],
    RESOURCE_SEARCH_RECORDS_EXPORT: ['xlsx', 'xls'],
    RESOURCE_BRAND: ['jpg', 'png', 'jpeg', 'gif'],
    RESOURCE_CLEARING: ['xlsx', 'xls'],
    RESOURCE_CLEARING_STATISTICS: ['jpg', 'png', 'jpeg', 'gif'],
    RESOURCE_MONTHLY_CLEARING_DNX: ['jpg', 'png', 'jpeg', 'gif'],
    RESOURCE_BANNER: ['jpg', 'png', 'jpeg', 'gif'],
    RESOURCE_AFTER_SALE: ['jpg', 'png', 'jpeg', 'gif'],
    RESOURCE_REVIEW_IMAGE: ['jpg', 'png', 'jpeg', 'gif'], 
    RESOURCE_REVIEW_VIDEO: ['mp4'],
    RESOURCE_COUNTRY_FLAGS: ['jpg', 'png', 'jpeg', 'gif'],
    RESOURCE_TOPIC_PAGE: ['jpg', 'png', 'jpeg', 'gif'],
    RESOURCE_SKIN: ['jpg', 'png', 'jpeg', 'gif'],
    RESOURCE_SALES_ORDER_EXCEL: ['xlsx', 'xls'],
    RESOURCE_PACKAGE_EXCEL: ['xlsx', 'xls'],
    RESOURCE_GOODS_PENDING_DISPATCH_EXCEL: ['xlsx', 'xls'],
    RESOURCE_REFUND_SLIP_EXCEL: ['xlsx', 'xls'],
    RESOURCE_IMAGE_SEARCH: ['jpg', 'png', 'jpeg', 'gif'],
    RESOURCE_AVATAR: ['jpg', 'png', 'jpeg', 'gif'],
    RESOURCE_GOODS_EXPORT: ['xlsx', 'xls'],
    RESOURCE_CATEGORY: ['jpg', 'png', 'jpeg', 'gif'],
    RESOURCE_APP_SHORTCUT_ICON: ['jpg', 'png', 'jpeg', 'gif'],
    RESOURCE_ADS_IMAGE: ['jpg', 'png', 'jpeg', 'gif'],
    RESOURCE_SPLASH_IMAGE: ['jpg', 'png', 'jpeg', 'gif'],
    RESOURCE_COMMISSION: ['jpg', 'jpeg', 'png',  'pdf', 'doc', 'docx'],
    RESOURCE_FILE_CACHE: ['json']
}

# 允许的文件大小
OBJECT_STORAGE_ALLOW_FILE_SIZE_DEFAULT = 30
OBJECT_STORAGE_ALLOW_FILE_SIZE = {
    RESOURCE_GOODS_VIDEO: 20
}

SIZE_1280_1280 = "{}_1280.{}"
SIZE_720_720 = "{}_720.{}"
SIZE_360_360 = "{}_360.{}"
SIZE_240_240 = "{}_240.{}"
SIZE_60_60 = "{}_60.{}"

OBJECT_STORAGE_SYSTEM_OBS = 1
OBJECT_STORAGE_SYSTEM_S3 = 2
