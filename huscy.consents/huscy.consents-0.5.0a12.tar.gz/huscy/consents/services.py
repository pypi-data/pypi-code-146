import jsonschema

from huscy.consents.models import Consent


TEXT_FRAGMENTS_SCHEMA = {
    "$defs": {
        "checkbox": {
            "type": "object",
            "properties": {
                "type": {"type": "string", "pattern": "checkbox"},
                "properties": {
                    "type": "object",
                    "properties": {
                        "text": {"type": "string"},
                        "required": {"type": "boolean"},
                    },
                    "required": ["text", "required"],
                },
            },
            "required": ["properties"],
        },
        "paragraph": {
            "type": "object",
            "properties": {
                "type": {"type": "string", "pattern": "paragraph"},
                "properties": {
                    "type": "object",
                    "properties": {
                        "text": {"type": "string"},
                        "boldface": {"type": "boolean"},
                    },
                    "required": ["text", "boldface"],
                },
            },
            "required": ["properties"],
        },
    },

    "type": "array",
    "items": {
        "anyOf": [
            {"$ref": "#/$defs/checkbox"},
            {"$ref": "#/$defs/paragraph"},
        ],
    },
    "minItems": 1,
}


def create_consent(name, text_fragments):
    jsonschema.validate(text_fragments, TEXT_FRAGMENTS_SCHEMA)
    return Consent.objects.create(name=name, text_fragments=text_fragments)


def update_consent(consent, name=None, text_fragments=None):
    consent.name = consent.name if name is None else name
    if text_fragments is not None:
        jsonschema.validate(text_fragments, TEXT_FRAGMENTS_SCHEMA)
        consent.text_fragments = text_fragments
    consent.save()
    return consent
