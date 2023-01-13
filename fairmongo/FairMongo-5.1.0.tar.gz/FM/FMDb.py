from pymongo.database import Database
from FM.FMClient import FMClient
from FM.FMC import FMC
from F.LOG import Log


Log = Log(f"DBDatabase")

"""
    -> THE MASTER BASE CLASS
        - The Database Instance Itself.
    -> Does not need a collection to be initiated.
"""
DATABASE = lambda host, db: FMDB.quick_init(host, db)
COLLECTION = lambda host, db, name: FMDB.quick_init(host, db).collection(name)

class FMDB(FMClient):
    db: Database = None
    collection_names = None

    @classmethod
    def quick_init(cls, host, db):
        newCls = cls()
        return newCls.connect(ip=host).database(db)

    def database(self, databaseName, dbclient:FMClient=None):
        if dbclient:
            self.client = dbclient.client
        if self.is_connected():
            self.db = self.client.get_database(databaseName)
            self.collection_names = self.db.list_collection_names()
            return self
        return None

    def collection(self, collectionName) -> FMC:
        cc = self.db.get_collection(collectionName)
        return FMC(cc)

    def list_collection_names(self):
        return self.db.list_collections()


if __name__ == '__main__':
    # clientOne = DBClient().connect("192.168.1.180", 27017)
    from FM.QueryHelper import Q
    dbone = FMDB().connect("192.168.1.180", 27017).database("research")
    results = dbone.collection("articles").base_query(Q.FIELD_EXISTENCE("category", True), limit=0)
    print(len(results))
