

class AO:
    MATCH = "$match"
    GROUP = "$group"
    TO_DATE = "$toDate"
    ADD_FIELDS = "$addFields"
    LIMIT = "$limit"
    SORT = "$sort"

class A(AO):
    MATCH = lambda matchQuery: { AO.MATCH: matchQuery }
    LIMIT = lambda value: { AO.LIMIT: value }
    SORT = lambda sortQuery: { AO.SORT: sortQuery }

class MATCH(A):

    MATCH_DATE_RANGE = lambda gte, lte: {"$match": {"$and": [JQ.DATE_PUB_GREATER_THAN(gte), JQ.DATE_PUB_LESS_THAN(lte)]}}
    MATCH_SEARCH = lambda searchTerm: {"$match": JQ.SEARCH_ALL(search_term=searchTerm)}
    MATCH_SINGLE_FIELD_VALUE = lambda field, value: {A.MATCH: {field: value}}
    MATCH_SINGLE_FIELD_EXISTS = lambda field, exists: {A.MATCH: Q.FIELD_EXISTENCE(field, exists)}
