from pymongo import MongoClient, bulk
from pymongo.database import Database
from FCM import MCServers
from FCM.MCCollection import MCCollection
from F import DICT, DATE
from F.CLASS import FairClass
from dateutil import parser
import datetime
from F.LOG import Log

s = " "
Log = Log(f"MCCore")

"""
    -> THE MASTER BASE CLASS
        - The Database Instance Itself.
    -> Does not need a collection to be initiated.
    -> Other Classes inherent this object.
"""

class MCCore(FairClass, MCCollection):
    core_connection_status = False
    core_client: MongoClient
    core_db: Database
    core_collection: Database = False
    core_bulk = bulk

    # -> !!MAIN CONSTRUCTOR!! <-
    def _constructor(self, url, databaseName):
        Log.className = f"MCore HOST=[ {MCServers.db_environment_name} ], DATABASE=[ {databaseName} ]"
        try:
            Log.i(f"Initiating MongoDB: URI={url}")
            self.core_client = MongoClient(host=url, connectTimeoutMS=10000)
            if not self.core_client:
                return False
            if self.is_connected():
                self.core_db = self.core_client.get_database(databaseName)
                return self
        except Exception as e:
            Log.e(f"Unable to initiate MongoDB: URI={url}", error=e)
            return False
        return False

    def connect(self, collectionName, dbUri=None, dbName=None):
        try:
            if not dbUri:
                dbUri = MCServers.MONGO_DATABASE_URI
                dbName = MCServers.db_name
            self._constructor(dbUri, dbName)
            self.set_ccollection(collectionName)
            self.mcollection = self.core_collection
            return self
        except Exception as e:
            Log.e("Failed to Connect to DB.", error=e)
            return False

    def is_connected(self) -> bool:
        try:
            info = self.core_client.server_info()
            if info:
                Log.d("MongoDB is Up.")
                self.core_connection_status = True
                return True
        except Exception as e:
            Log.e("MongoDB is Down.", error=e)
            self.core_connection_status = False
            return False
        return False

    def _get_collection(self, collection_name) -> Database:
        """
        INTERNAL/PRIVATE ONLY
        - DO NOT USE -
        """
        self.core_collection = self.core_db.get_collection(collection_name)
        return self.core_collection

    def set_ccollection(self, collection_name):
        """
        INTERNAL/PRIVATE ONLY
        - DO NOT USE -
        """
        self.construct_cc(self._get_collection(collection_name))

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

# if __name__ == '__main__':
#     c = MCore().constructor()
#     print(c)