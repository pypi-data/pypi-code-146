# ${copyright}

from itsimodels.core.field_decode import FieldDecoder


class BackupFieldDecoder(FieldDecoder):
    """Decodes data from an ITSI backup object into the appropriate model format"""

    def decode_field_name(self, field, field_name):
        return field.alias or field_name
