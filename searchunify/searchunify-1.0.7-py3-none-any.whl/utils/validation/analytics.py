from schema import Schema, And, Use, Optional, Regex

class AnalyticsValidator:
    def get_tiles_data(**args):
        schema = {
            'startDate': And(Use(str), Regex(r'^\d{4}\-(0[1-9]|1[012])\-(0[1-9]|[12][0-9]|3[01])$'), error="Date format should be YYYY-MM-DD"),
            'endDate': And(Use(str), Regex(r'^\d{4}\-(0[1-9]|1[012])\-(0[1-9]|[12][0-9]|3[01])$'), error="Date format should be YYYY-MM-DD"),
            Optional('searchClientId'): And(Use(str), Regex(r'^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$'), error="searchClientId format should be a uuid.")
        }
        Schema(schema).validate(args)

    def get_search_summary_chart(**args):
        schema = {
            'startDate': And(Use(str), Regex(r'^\d{4}\-(0[1-9]|1[012])\-(0[1-9]|[12][0-9]|3[01])$'), error="Date format should be YYYY-MM-DD"),
            'endDate': And(Use(str), Regex(r'^\d{4}\-(0[1-9]|1[012])\-(0[1-9]|[12][0-9]|3[01])$'), error="Date format should be YYYY-MM-DD"),
            Optional('searchClientId'): And(Use(str), Regex(r'^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$'), error="searchClientId format should be a uuid.")
        }
        Schema(schema).validate(args)

    def analytics_data_validation(**args):
        schema = {
            'startDate': And(Use(str), Regex(r'^\d{4}\-(0[1-9]|1[012])\-(0[1-9]|[12][0-9]|3[01])$'), error="Date format should be YYYY-MM-DD"),
            'endDate': And(Use(str), Regex(r'^\d{4}\-(0[1-9]|1[012])\-(0[1-9]|[12][0-9]|3[01])$'), error="Date format should be YYYY-MM-DD"),
            Optional('searchClientId'): And(Use(str), Regex(r'^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$'), error="searchClientId format should be a uuid."),
            'count': And(Use(int), lambda n: 0 < n <= 500, error="Count should be 1-500")
        }
        Schema(schema).validate(args)

    def search_session_by_case_uid_auth(**args):
        schema = {
            'startDate': And(Use(str), Regex(r'^\d{4}\-(0[1-9]|1[012])\-(0[1-9]|[12][0-9]|3[01])$'), error="Date format should be YYYY-MM-DD"),
            'endDate': And(Use(str), Regex(r'^\d{4}\-(0[1-9]|1[012])\-(0[1-9]|[12][0-9]|3[01])$'), error="Date format should be YYYY-MM-DD"),
            'caseUID': And(Use(str), lambda s: len(s) > 0, error="Case UID is required."),
            'count': And(Use(int), lambda n: 0 < n <= 500, error="Count should be 1-500")
        }
        Schema(schema).validate(args)

    def search_conversion_with_filters(**args):
        schema = {
            'startDate': And(Use(str), Regex(r'^\d{4}\-(0[1-9]|1[012])\-(0[1-9]|[12][0-9]|3[01])$'), error="Date format should be YYYY-MM-DD"),
            'endDate': And(Use(str), Regex(r'^\d{4}\-(0[1-9]|1[012])\-(0[1-9]|[12][0-9]|3[01])$'), error="Date format should be YYYY-MM-DD")
        }
        Schema(schema).validate(args)

    def search_conversion_by_sessionid(**args):
        schema = {
            'startDate': And(Use(str), Regex(r'^\d{4}\-(0[1-9]|1[012])\-(0[1-9]|[12][0-9]|3[01])$'), error="Date format should be YYYY-MM-DD"),
            'endDate': And(Use(str), Regex(r'^\d{4}\-(0[1-9]|1[012])\-(0[1-9]|[12][0-9]|3[01])$'), error="Date format should be YYYY-MM-DD"),
            'count': And(Use(int), lambda n: 0 < n <= 500, error="Count should be 1-500"),
            'sessionId': And(Use(str), lambda s: len(s) > 5, error="sessionId is required."),
            Optional('searchClientId'): And(Use(str), Regex(r'^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$'), error="searchClientId format should be a uuid.")
        }
        Schema(schema).validate(args)

    def get_search_session_by_search_sessionid(**args):
        schema = {
            'startDate': And(Use(str), Regex(r'^\d{4}\-(0[1-9]|1[012])\-(0[1-9]|[12][0-9]|3[01])$'), error="Date format should be YYYY-MM-DD"),
            'endDate': And(Use(str), Regex(r'^\d{4}\-(0[1-9]|1[012])\-(0[1-9]|[12][0-9]|3[01])$'), error="Date format should be YYYY-MM-DD"),
            'count': And(Use(int), lambda n: 0 < n <= 500, error="Count should be 1-500"),
            'sessionId': And(Use(str), lambda s: len(s) > 5, error="sessionId is required."),
            Optional('pageNumber'): And(Use(int), lambda n: n >= 0, error="Invalid page number."),
            Optional('searchClientId'): And(Use(str), Regex(r'^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$'), error="searchClientId format should be a uuid.")
        }
        Schema(schema).validate(args)

    def get_discussions_ready_to_become_article(**args):
        schema = {
            'startDate': And(Use(str), Regex(r'^\d{4}\-(0[1-9]|1[012])\-(0[1-9]|[12][0-9]|3[01])$'), error="Date format should be YYYY-MM-DD"),
            'endDate': And(Use(str), Regex(r'^\d{4}\-(0[1-9]|1[012])\-(0[1-9]|[12][0-9]|3[01])$'), error="Date format should be YYYY-MM-DD"),
            'count': And(Use(int), lambda n: 0 < n <= 500, error="Count should be 1-500"),
            Optional('internalUser'): str,
            Optional('searchClientId'): And(Use(str), Regex(r'^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$'), error="searchClientId format should be a uuid.")
        }
        Schema(schema).validate(args)

    def case_created_validation(**args):
        schema = {
            'internalUser': str,
            'searchType': str,
            'startDate': And(Use(str), Regex(r'^\d{4}\-(0[1-9]|1[012])\-(0[1-9]|[12][0-9]|3[01])$'), error="Date format should be YYYY-MM-DD"),
            'endDate': And(Use(str), Regex(r'^\d{4}\-(0[1-9]|1[012])\-(0[1-9]|[12][0-9]|3[01])$'), error="Date format should be YYYY-MM-DD"),
            'searchClientId': And(Use(str), Regex(r'^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$'), error="searchClientId format should be a uuid."),
            Optional('offset'): And(Use(int), lambda n: n > 0, error="offset should be greater than 0."),
            Optional('count'): And(Use(int), lambda n: 0 < n <= 500, error="Count should be 1-500")
        }
        Schema(schema).validate(args)

    def get_attached_articles(**args):
        schema = {
            'internalUser': str,
            'startDate': And(Use(str), Regex(r'^\d{4}\-(0[1-9]|1[012])\-(0[1-9]|[12][0-9]|3[01])$'), error="Date format should be YYYY-MM-DD"),
            'endDate': And(Use(str), Regex(r'^\d{4}\-(0[1-9]|1[012])\-(0[1-9]|[12][0-9]|3[01])$'), error="Date format should be YYYY-MM-DD"),
            'searchClientId': And(Use(str), Regex(r'^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$'), error="searchClientId format should be a uuid."),
            Optional('offset'): And(Use(int), lambda n: n > 0, error="offset should be greater than 0."),
            Optional('count'): And(Use(int), lambda n: 0 < n <= 500, error="Count should be 1-500")
        }
        Schema(schema).validate(args)

    def get_attached_on_case(**args):
        schema = {
            'url': And(Use(str), Regex(r"(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'\".,<>?«»“”‘’]))"), error="Invalid Instance URL."),
            'startDate': And(Use(str), Regex(r'^\d{4}\-(0[1-9]|1[012])\-(0[1-9]|[12][0-9]|3[01])$'), error="Date format should be YYYY-MM-DD"),
            'endDate': And(Use(str), Regex(r'^\d{4}\-(0[1-9]|1[012])\-(0[1-9]|[12][0-9]|3[01])$'), error="Date format should be YYYY-MM-DD"),
            'searchClientId': And(Use(str), Regex(r'^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$'), error="searchClientId format should be a uuid."),
            Optional('offset'): And(Use(int), lambda n: n > 0, error="offset should be greater than 0."),
            Optional('count'): And(Use(int), lambda n: 0 < n <= 500, error="Count should be 1-500")
        }
        Schema(schema).validate(args)
