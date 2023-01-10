"""Constants"""

from typing import List

DEFAULT_EMAIL_DOMAIN = "icloud.com"

# For retrying connection after timeouts and errors
MAX_RETRIES = 5
WAIT_SECONDS = 5

MASTER_RECORD_TYPE = "CPLMaster"

# original photos and videos have this version.
ORIGINAL_MEDIA = "resOriginalRes"

# only live photos have this version.
ORIGINAL_LIVE = "resOriginalVidComplRes"

# only videos have this version.
# videos with special effects (e.g., slo-mo)
MEDIUM_VIDEO = "resVidMedRes"

# edited photos and video thumbnails have this version.
EDITED_PHOTO = "resJPEGFullRes"
EDITED_VIDEO = "resVidFullRes"

DOWNLOAD_FORMATS: List[str] = [
    ORIGINAL_MEDIA,
    ORIGINAL_LIVE,
    EDITED_PHOTO,
    EDITED_VIDEO,
    MEDIUM_VIDEO,
]
DOWNLOAD_FORMATS.extend([x + "-edit" for x in DOWNLOAD_FORMATS])
