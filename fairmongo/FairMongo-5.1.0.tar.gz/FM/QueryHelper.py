import datetime
import json
from bson import ObjectId
from dateutil import parser

from F import DATE, DICT
from F.LOG import Log

DESCENDING = -1
ASCENDING = 1
Log = Log("QueryHelper")
s = " "
"""
    -> Master Base Query Class/Object/Helper
"""

""" Aggregate Operators """
class AO:
    MATCH = "$match"
    GROUP = "$group"
    TO_DATE = "$toDate"
    ADD_FIELDS = "$addFields"
    LIMIT = "$limit"
    SORT = "$sort"

""" Aggregate """
class A(AO):
    MATCH = lambda matchQuery: { AO.MATCH: matchQuery }
    LIMIT = lambda value: { AO.LIMIT: value }
    SORT = lambda sortQuery: { AO.SORT: sortQuery }

""" Aggregate Pipelines """
class AP(A):
    SORT_by_SINGLE_FIELD = lambda fieldName: { AO.SORT: { fieldName: DESCENDING } }

BUILD_PIPELINE = lambda *stages: [s for s in stages]

""" Regex """
class R:
    SEARCH = lambda search_term: fr'.*{search_term}.*'
    SEARCH_STRICT = lambda search_term: fr'\b{search_term}\b'

""" Operators """
class O:
    OBJECT_ID = lambda id: id if type(id) in [ObjectId] else ObjectId(id)
    REGEX = "$regex"
    SEARCH = "$search"
    SET = "$set"
    PULL = "$pull"
    PUll_ALL = "$pullAll"
    OR = "$or"
    NOR = "$nor"
    AND = "$and"
    IN = "$in"
    WHERE = "$where"
    ADD_TO_SET = "$addToSet"
    EACH = "$each"
    TYPE = "$type"
    EQUALS = "$eq"
    NOT_EQUALS = "$ne"
    EXISTS = "$exists"
    NOT = "$not"
    SIZE = "$size"
    OPTIONS = '$options'
    i_OPTION = 'i'
    GREATER_THAN_OR_EQUAL = "$gte"
    LESS_THAN_OR_EQUAL = "$lte"
    GTE = GREATER_THAN_OR_EQUAL
    LTE = LESS_THAN_OR_EQUAL

"""
check if ObjectId

single_query = { "_id": Q.NOT_EQUALS(O.TO_OBJECT_ID(id)) }
final_query = Q.OR([single_query])

"""

""" Query """
class Q:
    BASE = lambda key, value: {key: value}
    COMMENTS_AUTHOR = lambda key, value: { "this.comments.author": value }
    BASE_TWO = lambda key1, value1, key2, value2: {key1: value1, key2: value2}
    OR = lambda list_of_queries: {O.OR: list_of_queries}
    AND = lambda list_of_queries: {O.AND: list_of_queries}
    REGEX = lambda search_term: Q.BASE_TWO(O.REGEX, R.SEARCH(search_term), O.OPTIONS, 'i')
    REGEX_STRICT = lambda search_term: Q.BASE_TWO(O.REGEX, R.SEARCH_STRICT(search_term), O.OPTIONS, 'i')
    SEARCH = lambda field, search_term: Q.BASE(field, Q.REGEX(search_term))
    SEARCH_EMBEDDED = lambda fieldOne, fieldTwo, search_term: Q.BASE(f"{fieldOne}.{fieldTwo}", Q.REGEX(search_term))
    SEARCH_STRICT = lambda field, search_term: Q.BASE(field, Q.REGEX_STRICT(search_term))
    LTE = lambda value: Q.BASE(O.LESS_THAN_OR_EQUAL, value)
    SIZE = lambda value: Q.BASE(O.SET, value)
    EQUALS = lambda value: Q.BASE(O.EQUALS, value)
    NOT_EQUALS = lambda value: Q.BASE(O.NOT_EQUALS, value)
    SET = lambda field, list_value: Q.BASE(O.SET, Q.BASE(field, list_value))
    PULL = lambda value: Q.BASE(O.PULL, value)
    ADD_TO_SET = lambda field, list_value: Q.BASE(O.ADD_TO_SET, Q.BASE(field, Q.BASE(O.EACH, list_value)))
    LESS_THAN_OR_EQUAL = lambda value: Q.BASE(O.LESS_THAN_OR_EQUAL, value)
    GREATER_THAN_OR_EQUAL = lambda value: Q.BASE(O.GREATER_THAN_OR_EQUAL, value)
    FIELD_EXISTENCE = lambda fieldName, doesExist: Q.BASE(fieldName, Q.BASE(O.EXISTS, doesExist))
    FIELD_EQUALS = lambda field, value: Q.BASE(field, Q.EQUALS(value))
    FIELD_NOT_EQUALS = lambda field, value: Q.BASE(field, Q.NOT_EQUALS(value))



class QDict(Q, O):
    SET_FIELD_KEY = lambda field, key, value: { O.SET: { f"{field}.{key}": value } }
    # set = { O.SET: { "fieldName.keyName": "3", "fieldName2.keyName2": "2" } }

    # def update_dict(self, field, key, value):

""" Query Builder """
class QBuilder(Q, O, R):
    query_builder = {}

    def add_to_query_builder(self, key, value):
        self.query_builder[key] = value
    def get_built_query(self):
        return self.query_builder
    def clear_query_builder(self):
        self.query_builder = {}
    def print_built_query(self):
        obj = json.dumps(self.query_builder, sort_keys=True, indent=4, default=str)
        print(obj)

""" Query Helpers """
class QHelpers:

    @staticmethod
    def parse_date_for_query(date: str) -> datetime:
        return datetime.datetime.strptime(date, "%B %d %Y")

    """ OUT of database -> OFFICIAL DATE CONVERSION FROM DATABASE ENTRY <- """

    @staticmethod
    def from_db_date(str_date):
        date_obj = parser.parse(str_date)
        return date_obj

    """ INTO database -> OFFICIAL DATE CONVERSION FOR DATABASE ENTRY <- """

    @staticmethod
    def to_db_date(t=None):
        if t is None:
            t = datetime.datetime.now()
        date = str(t.strftime("%B")) + s + str(t.strftime("%d")) + s + str(t.strftime("%Y"))
        return date

    @staticmethod
    def get_now_date():
        return DATE.get_now_month_day_year_str()

    @staticmethod
    def parse_date(obj=None):
        if type(obj) is str:
            obj = DATE.parse_str_to_datetime(obj)
        elif type(obj) is list:
            return None
        p_date = str(obj.strftime("%B")) + s + str(obj.strftime("%d")) + s + str(obj.strftime("%Y"))
        return p_date

    @staticmethod
    def to_list(cursor):
        return list(cursor)

    @staticmethod
    def to_counted_dict(cursor):
        """ DEPRECATED """
        result_dict = {}
        for item in cursor:
            _id = DICT.get("_id", item)
            raw = DICT.get("raw_hookups", item)
            count = len(raw)
            result_dict[_id] = {"count": count,
                                "raw_hookups": raw}
        return result_dict

    @staticmethod
    def cursor_count(cursor) -> int:
        return len(list(cursor))

