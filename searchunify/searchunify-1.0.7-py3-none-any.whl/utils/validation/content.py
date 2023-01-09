from schema import Schema, And, Use, Optional

class ContentValidator:
    def content_source_id_validation(**args):
        schema = {
            'contentSourceId': And(Use(str), lambda s: len(s) > 0, error="contentSourceId is required.")
        }
        Schema(schema).validate(args)

    def get_object_specific_data(**args):
        schema = {
            'contentSourceId': And(Use(str), lambda s: len(s) > 0, error="contentSourceId is required."),
            'objectId': And(Use(str), lambda s: len(s) > 0, error="objectId is required."),
            Optional('offset'): And(Use(int), lambda n: n >= 0, error="offset value should be greater than or equal to 0."),
            Optional('size'): int,
        }
        Schema(schema).validate(args)

    def get_object_specific_data_with_id(**args):
        schema = {
            'contentSourceId': And(Use(str), lambda s: len(s) > 0, error="contentSourceId is required."),
            'objectId': And(Use(str), lambda s: len(s) > 0, error="objectId is required."),
            'documentId': And(Use(str), lambda s: len(s) > 0, error="documentId is required.")
        }
        Schema(schema).validate(args)

    def update_doucment_by_id(**args):
        schema = {
            'contentSourceId': And(Use(str), lambda s: len(s) > 0, error="contentSourceId is required."),
            'objectId': And(Use(str), lambda s: len(s) > 0, error="objectId is required."),
            'documentId': And(Use(str), lambda s: len(s) > 0, error="documentId is required."),
            'data': dict
        }
        Schema(schema).validate(args)

    def upload_data(**args):
        schema = {
            'contentSourceId': And(Use(str), lambda s: len(s) > 0, error="contentSourceId is required."),
            'objectId': And(Use(str), lambda s: len(s) > 0, error="objectId is required."),
            'data': list
        }
        Schema(schema).validate(args)
