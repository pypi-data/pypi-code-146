from schema import Schema, And, Use, Regex

class SearchValidator:
    def get_search_results(**args):
        schema = {
            'searchString': str,
            'uid': And(Use(str), Regex(r'^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$'), error="Invalid uuid format for uid.")
        }
        Schema(schema, ignore_extra_keys=True).validate(args)
