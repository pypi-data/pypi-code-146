# import time
from F import LIST, DICT
from F.LOG import Log
Log = Log("MCollection")

"""
    -> BASE CLASS
        - Collection Instance Object on top of MCore.
    -> Does not need a collection to be initiated.
    -> Other Classes inherent this object.
"""

class MCCollection:
    mcollection_name: str = None
    mcollection = None

    def construct_cc(self, collection):
        self.mcollection_name = str(collection)
        self.mcollection = collection

    def get_document_count(self):
        return self.mcollection.estimated_document_count()

    def base_aggregate(self, pipeline, allowDiskUse=True):
        if not self.mcollection:
            return False
        results = self.mcollection.aggregate(pipeline, allowDiskUse=allowDiskUse)
        results = self.to_list(results)
        if results and len(results) > 0:
            return results
        return False

    def base_query(self, kwargs, page=0, limit=100):
        if not self.mcollection:
            return False
        if limit and page >= 0:
            results = self.mcollection.find(kwargs).skip(page).limit(limit)
        else:
            results = self.mcollection.find(kwargs)
        results = self.to_list(results)
        if results and len(results) > 0:
            return results
        return False

    def base_query_unlimited(self, kwargs):
        if not self.mcollection:
            return False
        results = self.mcollection.find(kwargs)
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

    @staticmethod
    def to_list(cursor):
        return list(cursor)

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
            Log.w("Object Exists in Database Already. Skipping...")
            return True
        Log.v("Object Does Not Exist in Database.")
        return False

    def add_records(self, list_of_objects):
        """ Each Object should be JSON Format """
        list_of_objects = LIST.flatten(list_of_objects)
        Log.w(f"Beginning Add Records Queue. COUNT=[ {len(list_of_objects)} ]")
        for objectItem in list_of_objects:
            article_exists = self.record_exists(objectItem)
            if not article_exists:
                self.insert_record(objectItem)
        Log.w(f"Finished Add Records Queue.")

    def add_records_field_match(self, list_of_objects, fieldName, ignoreExists=False):
        """ Each Object should be JSON Format """
        list_of_objects = LIST.flatten(list_of_objects)
        Log.w(f"Beginning Add Records Queue. COUNT=[ {len(list_of_objects)} ]")
        for objectItem in list_of_objects:
            fieldValue = DICT.get(fieldName, objectItem, default=False)
            if ignoreExists:
                self.insert_record(objectItem)
                continue
            article_exists = self.record_exists_by_field_match(fieldName, fieldValue)
            if not article_exists:
                self.insert_record(objectItem)
        Log.w(f"Finished Add Records Queue.")

    def insert_record(self, kwargs):
        try:
            # time.sleep(1)
            self.mcollection.insert_one(kwargs)
            Log.s(f"NEW Record created in DB=[ {self.mcollection_name} ]")
            return True
        except Exception as e:
            Log.e(f"Failed to save record in DB=[ {self.mcollection_name} ]", error=e)
            return False

    def update_record(self, findQuery: dict, updateQuery: dict, upsert=True):
        try:
            # time.sleep(1)
            self.mcollection.update_one( findQuery, { "$set": updateQuery }, upsert=upsert )
            Log.s(f"UPDATED Record in DB=[ {self.mcollection_name} ]")
            return True
        except Exception as e:
            Log.e(f"Failed to save record in DB=[ {self.mcollection_name} ]", error=e)
            return False

    def replace_record(self, findQuery: dict, updateQuery: dict, upsert=True):
        try:
            # time.sleep(1)
            self.mcollection.replace_one( findQuery, { "$set": updateQuery }, upsert=upsert )
            Log.s(f"REPLACED Record in DB=[ {self.mcollection_name} ]")
            return True
        except Exception as e:
            Log.e(f"Failed to save record in DB=[ {self.mcollection_name} ]", error=e)
            return False

    def update_many_records(self, findQuery: dict, updateQueries: list, upsert=True):
        try:
            # time.sleep(1)
            self.mcollection.update_many( findQuery, updateQueries, upsert=upsert )
            Log.s(f"UPDATED Record in DB=[ {self.mcollection_name} ]")
            return True
        except Exception as e:
            Log.e(f"Failed to save record in DB=[ {self.mcollection_name} ]", error=e)
            return False

    def remove_record(self, kwargs):
        try:
            # time.sleep(1)
            self.mcollection.delete_one(kwargs)
            Log.s(f"Removed Record in DB=[ {self.mcollection_name} ]")
            return True
        except Exception as e:
            Log.e(f"Failed to remove record in DB=[ {self.mcollection_name} ]", error=e)
            return False
