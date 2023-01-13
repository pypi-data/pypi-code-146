# cerberus schema for plugin metadata
plugin_metadata_schema = {
    # mandatory
    "hash": {
        "type": "string",
        "required": True,
        "check_with": "is_hex"
    },
    "name": {
        "type": "string",
        "required": True,
        "check_with": "is_alphanumeric"
    },
    "description": {
        "type": "string",
        "required": True,
    },
    "author": {
        "type": "string",
        "required": True,
        "check_with": "is_author"
    },
    "version": {
        "type": "string",
        "required": True,
        "check_with": "is_semver"
    },
    "license": {
        "type": "string",
        "required": True,
    },
    "url": {
        "type": "string",
        "required": True,
        "check_with": "is_url"
    },
    # optional
    "category": {
        "type": "string",
        "required": False,
        "check_with": "is_alphanumeric"
    },
    "tags": {
        "type": "string",
        "required": False,
        "check_with": "is_list"
    },
}
