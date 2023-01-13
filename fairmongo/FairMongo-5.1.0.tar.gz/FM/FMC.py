from F import LIST, DICT, TYPE
from bson import ObjectId
from FM.FMRecord import Records, Record
from FM.QueryHelper import QHelpers, Q
from F.LOG import Log

s = " "
Log = Log(f"DBCollection")

"""
    -> THE MASTER BASE CLASS
        - The Database Instance Itself.
    -> Does not need a collection to be initiated.
    -> Other Classes inherent this object.
"""
SEARCH_ALL = lambda search_term: Q.OR([Q.SEARCH("FieldName", search_term), Q.SEARCH("FieldName", search_term)])
# SEARCH_BY_DATE_RANGE = lambda searchTerm, gte, lte, limit: [
#             STAGE_MATCH.MATCH_DATE_RANGE(gte, lte),
#             STAGE_MATCH.MATCH_SEARCH(searchTerm),
#             STAGE_MATCH.LIMIT(limit)
#     ]

class FMC(QHelpers):
    core_collection = None

    def __init__(self, collection):
        self.core_collection = collection

    def get_document_count(self):
        return self.core_collection.estimated_document_count()

    """
        - Queries
    """
    def base_aggregate(self, pipeline, allowDiskUse=True):
        if not self.core_collection:
            return False
        results = self.core_collection.aggregate(pipeline, allowDiskUse=allowDiskUse)
        results = self.to_list(results)
        if results and len(results) > 0:
            return results
        return False

    def base_query(self, kwargs, page=0, limit=100):
        if not self.core_collection:
            return False
        if limit and page >= 0:
            results = self.core_collection.find(kwargs).skip(page).limit(limit)
        else:
            results = self.core_collection.find(kwargs)
        results = self.to_list(results)
        if results and len(results) > 0:
            return results
        return False

    def base_query_unlimited(self, kwargs):
        if not self.core_collection:
            return False
        results = self.core_collection.find(kwargs)
        results = self.to_list(results)
        if results and len(results) > 0:
            return results
        return False
    def get_field_names(self):
        fields = []
        oneResult = self.base_query({}, 0, 1)
        oneDoc = LIST.get(0, oneResult)
        for doc in oneDoc:
            fields.append(doc)
        return fields

    def search_all_fields(self, search_term:str):
        field_names = self.get_field_names()
        or_list = []
        for fname in field_names:
            or_list.append(Q.SEARCH(fname, search_term))
        query = Q.OR(or_list)
        self.base_query(query)

    # def search_by_date_range(self, searchTerm, gte, lte, limit=1000):
    #     gte2 = DATE.TO_DATETIME(gte)
    #     lte2 = DATE.TO_DATETIME(lte)
    #     return self.base_aggregate(Pipelines.SEARCH_BY_DATE_RANGE(searchTerm=searchTerm, gte=gte2, lte=lte2, limit=limit), allowDiskUse=True)

    def search_field(self, search_term, field_name, page=0, limit=100):
        return self.base_query(kwargs=Q.SEARCH(field_name, search_term), page=page, limit=limit)

    """
        -> Insert / Update / Remove
    """
    def record_exists(self, recordIn) -> bool:
        temp = self.base_query(recordIn)
        if temp:
            Log.w("Object Exists in Database Already. Skipping...")
            return True
        Log.v("Object Does Not Exist in Database.")
        return False

    def record_exists_by_field_match(self, field, value) -> bool:
        temp = self.base_query({field:value})
        if temp:
            Log.d("Object Exists in Database Already. Skipping...")
            return True
        Log.v("Object Does Not Exist in Database.")
        return False

    def add_records(self, list_of_objects, ignoreExists=False):
        """ Each Object should be JSON Format """
        list_of_objects = LIST.flatten(list_of_objects)
        Log.w(f"Beginning Add Records Queue. COUNT=[ {len(list_of_objects)} ]")
        for objectItem in Log.ProgressBarYielder(list_of_objects, prefix="Saving Records to MongoDB"):
            if not ignoreExists:
                record_exists = self.record_exists(objectItem)
                if not record_exists:
                    self.insert_record(objectItem)
            else:
                self.insert_record(objectItem)
        Log.w(f"Finished Add Records Queue.")

    def add_records_field_match(self, list_of_objects, fieldName, ignoreExists=False):
        """ Each Object should be JSON Format """
        list_of_objects = LIST.flatten(list_of_objects)
        count = 0
        fullCount = len(list_of_objects)
        Log.w(f"Beginning Add Records Queue. COUNT=[ {fullCount} ]")
        for objectItem in Log.ProgressBarYielder(list_of_objects, prefix=f"Adding {fullCount} Records..."):
            count += 1
            fieldValue = DICT.get(fieldName, objectItem, default=False)
            if ignoreExists:
                self.insert_record(objectItem)
                continue
            record_exists = self.record_exists_by_field_match(fieldName, fieldValue)
            if not record_exists:
                self.insert_record(objectItem)
        Log.w(f"Finished Add Records Queue.")

    def addUpdate_records(self, list_of_objects, ignoreExists=False):
        """ Each Object should be JSON Format """
        list_of_objects = LIST.flatten(list_of_objects)
        Log.w(f"Beginning Add Records Queue. COUNT=[ {len(list_of_objects)} ]")
        for objectItem in Log.ProgressBarYielder(list_of_objects, prefix="Saving Records to MongoDB"):
            potential_id = DICT.get("_id", objectItem, False)
            if potential_id:
                findQuery = {"_id": ObjectId(potential_id)}
                self.core_collection.update_record(findQuery, objectItem)
            else:
                self.insert_record(objectItem)
        Log.w(f"Finished Add Records Queue.")

    def smart_AddUpdate(self, obj_or_objs):
        if TYPE.is_types(obj_or_objs, list, Records, set):
            return self._smart_AddUpdate_records(obj_or_objs)
        Log.w(f"Smart AddUpdate Single Record.")
        return self._smart_AddUpdate_record(obj_or_objs)
    def _smart_AddUpdate_records(self, list_of_records):
        Log.w(f"Beginning Smart Queue.")
        for objectItem in Log.ProgressBarYielder(list_of_records, prefix="Saving Records to MongoDB"):
            self._smart_AddUpdate_record(objectItem)
        Log.w(f"Finished Smart Queue.")
    def _smart_AddUpdate_record(self, record):
        """ either a Records object or List object """
        if TYPE.is_types(record, Record):
            record: Record
            update_record = record.export()
        else:
            update_record = record
        potential_id = DICT.get("_id", update_record, "")
        findQuery = {"_id": ObjectId(potential_id)}
        return self.core_collection.update_record(findQuery, update_record)

    def insert_record(self, kwargs):
        try:
            # time.sleep(1)
            self.core_collection.insert_one(kwargs)
            # Log.d(f"NEW Record created in DB=[ {self.core_collection} ]")
            return True
        except Exception as e:
            Log.e(f"Failed to save record in DB=[ {self.core_collection} ]", error=e)
            return False

    def update_record(self, findQuery: dict, updateQuery: dict, upsert=True):
        try:
            # time.sleep(1)
            self.core_collection.update_one( findQuery, { "$set": updateQuery }, upsert=upsert )
            # Log.s(f"UPDATED Record in DB=[ {self.core_collection} ]")
            return True
        except Exception as e:
            Log.e(f"Failed to save record in DB=[ {self.core_collection} ]", error=e)
            return False

    def replace_record(self, findQuery: dict, updateQuery: dict, upsert=True):
        try:
            # time.sleep(1)
            self.core_collection.replace_one( findQuery, { "$set": updateQuery }, upsert=upsert )
            Log.s(f"REPLACED Record in DB=[ {self.core_collection} ]")
            return True
        except Exception as e:
            Log.e(f"Failed to save record in DB=[ {self.core_collection} ]", error=e)
            return False

    def update_many_records(self, findQuery: dict, updateQueries: list, upsert=True):
        """ Give List of Obj's that will all be updated by one Find Query. """
        try:
            # time.sleep(1)
            self.core_collection.update_many( findQuery, updateQueries, upsert=upsert )
            Log.s(f"UPDATED Record in DB=[ {self.core_collection} ]")
            return True
        except Exception as e:
            Log.e(f"Failed to save record in DB=[ {self.core_collection} ]", error=e)
            return False

    def remove_record(self, kwargs):
        try:
            # time.sleep(1)
            self.core_collection.delete_one(kwargs)
            Log.s(f"Removed Record in DB=[ {self.core_collection} ]")
            return True
        except Exception as e:
            Log.e(f"Failed to remove record in DB=[ {self.core_collection} ]", error=e)
            return False
