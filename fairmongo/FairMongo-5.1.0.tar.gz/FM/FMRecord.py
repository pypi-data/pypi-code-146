from F import DICT, DATE
from F.TYPE.Dict import fict
from F.TYPE.List import fist
# from FM import FMDb, FMC
# from FM.FMDb import FMDB

""" Smart dict:type wrapper for Single MongoDB Record."""
class Record(fict):
    _id = ""
    fields = []
    original_record = None

    def __init__(self, record, **kwargs):
        super().__init__(**kwargs)
        self.original_record = record
        self.import_record(record)

    def import_record(self, record:dict):
        if not record:
            return None
        self._id = DICT.get("_id", record, "Unknown")
        self._add_fields(record)
        self.update(record)

    def _add_fields(self, record:dict):
        for key in record.keys():
            self.fields.append(key)

    def get_field(self, fieldName):
        return self[fieldName]

    def get_embeddedDict(self, fieldName, key):
        obj: dict = self.get_field(fieldName)
        embedded_obj = DICT.get(key, obj, None)
        return embedded_obj

    def update_updatedDate(self):
        self["updatedDate"] = DATE.TODAY

    def update_field(self, fieldName, value):
        self[fieldName] = value
        self.update_updatedDate()

    def export(self, isUpdate=False):
        if isUpdate:
            self.update_updatedDate()
        result = {}
        for f in self.fields:
            result[f] = self[f]
        return result

    # def smartAddUpdate(self, fmdbObject:FMDB):
    #     dbCollection: FMC = fmdbObject.collection(self.collection_name)
    #     dbCollection.smart_AddUpdate(self)



""" Smart list:type wrapper for List of MongoDB Records."""
class Records(fist):
    database_name = ""
    collection_name = ""

    def set_database_name(self, database_name):
        self.database_name = database_name

    def set_collection_name(self, collection_name):
        self.collection_name = collection_name

    def import_records(self, records:list):
        for rec in records:
            newR = Record(rec)
            self.append(newR)

    def loop_exported(self) -> dict:
        for rec in self:
            rec: Record
            yield rec.export()

    def loop_records(self) -> Record:
        for rec in self:
            rec: Record
            yield rec

    def to_exported_list(self) -> [dict]:
        results = []
        for item in self:
            results.append(item.export())
        return results

    def flatten(self):
        pass

    # def smartAddUpdateRecords(self, **kwargs):
    #     dbCollection: FMC = FMDB(kwargs).database(self.database_name).collection(self.collection_name)
    #     dbCollection.smart_AddUpdate(self)



"""
db = "research"
collection = "articles

fields = [ "_id", "title", "date" ]
single_article = {"_id": "1234", "title": "hey there", "date": "july 24 2022"}
"""