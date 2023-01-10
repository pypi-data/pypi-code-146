from itsicli.content_packs.validate.validate_config import ValidateConfig
from itsicli.content_packs.validate.validate_icon import ValidateIcon
from itsicli.content_packs.validate.validate_metadata import ValidateMetadata
from itsicli.content_packs.validate.validate_screenshots import ValidateScreenshots

VALIDATORS = [
    ValidateConfig,
    ValidateIcon,
    ValidateMetadata,
    ValidateScreenshots
]
