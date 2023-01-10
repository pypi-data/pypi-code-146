import mysql.connector as connector
import os
import uuid

def get_db_connection():
    from  mlmd import gservice_dao
    mlmd_config = gservice_dao.get_secret("MLMD_CONFIG")
    connection = connector.connect(
    host=mlmd_config.get("MLMD_HOST"),
    user=mlmd_config.get("MLMD_USER"),
    password=mlmd_config.get("MLMD_PASSWORD"),
    database=mlmd_config.get("MLMD_DB")
    )
    return connection

connection = get_db_connection()
if connection is None:
    raise Exception("Cannot connect to mlmd database")

def ensure_connection():
    global connection
    if not connection.is_connected():
        connection.reconnect(3) 

def execute_query(query, parameters_array, commit=True):
    global connection
    ensure_connection()
    dbcursor = connection.cursor()
    dbcursor.executemany(query, parameters_array)
    if commit:
        connection.commit()
    r = dbcursor.rowcount
    dbcursor.close()
    return r

def execute_select_query(query, parameters, commit=True):
    global connection
    ensure_connection()
    dbcursor = connection.cursor()
    dbcursor.execute(query, parameters)
    r = dbcursor.fetchall()
    if commit:
        connection.commit()
    dbcursor.close()
    return r

def insert_image_metadata_bulk(obj_arr, return_ids=False):
    """Insert multiple image image metadata

        Parameters:
        obj_arr (array): array of tuple of (image_name, tenant_id, dataset_id)

        Returns:
        Any
    """
    if len(obj_arr) <= 0:
        print("Nothing to insert")
        return False

    _query = """INSERT INTO image_metadata(image_name, tenant_id, dataset_id, annotation, metadata) VALUES (%s, %s, %s, %s, %s) 
                ON DUPLICATE KEY UPDATE tenant_id=VALUES(tenant_id), dataset_id=VALUES(dataset_id), annotation=VALUES(annotation)"""
    if return_ids:
        global connection
        ensure_connection()
        connection.start_transaction()
        last_id = 0
        inserted_last_id_struct = execute_select_query("SELECT image_id from image_metadata order by image_id desc limit 1", None, commit=False)
        if len(inserted_last_id_struct) > 0:
            last_id = inserted_last_id_struct[0][0]
        execute_query(_query, obj_arr, commit=False)
        image_id_struct = execute_select_query("SELECT image_id FROM image_metadata where image_id > %s", (last_id,))
        connection.commit()
        return [image_id for (image_id,) in image_id_struct]

    return execute_query(_query, obj_arr)

def update_image_metadata_bulk(obj_arr):
    """Insert multiple image image metadata

        Parameters:
        obj_arr (array): array of tuple of (metadata, dataset_id, image_name)

        Returns:
        Any
    """
    if len(obj_arr) <= 0:
        print("Nothing to insert")
        return False

    _query = """UPDATE image_metadata set metadata=%s where dataset_id=%s and image_name=%s"""
    return execute_query(_query, obj_arr)

def update_image_annotation_bulk(obj_arr):
    """Insert multiple image image metadata

        Parameters:
        obj_arr (array): array of tuple of (annotation, dataset_id, image_name)

        Returns:
        Any
    """
    if len(obj_arr) <= 0:
        print("Nothing to insert")
        return False

    _query = """UPDATE image_metadata set annotation=%s where dataset_id=%s and image_name=%s"""
    return execute_query(_query, obj_arr)

def insert_image_log_bulk(obj_arr):
    """Insert multiple image log

        Parameters:
        obj_arr (array): array of tuple of (image_id, execution_id, version_id, dataset_id)

        Returns:
        Any
    """
    return execute_query("INSERT INTO image_log(image_id, execution_id, version_id, dataset_id) VALUES (%s, %s, %s, %s)", obj_arr)

def insert_tenants(obj_arr):
    return execute_query("INSERT IGNORE INTO tenant(tenant_name) VALUES (%s)", obj_arr)

def get_image_executions_by_version(version_id, metadata_filter=None):
    params = (version_id,)
    metadata_conditions = []
    allowed_fields = ["annotation", "tenant_id"]
    restricted_chars = ["-", "'"]
    if metadata_filter is not None and len(metadata_filter)>0:
        if not isinstance(metadata_filter, list):
            raise Exception("Invalid metadata filter condition. Expecting list instead of {}".format(metadata_filter))
        for item in metadata_filter:
            if not isinstance(item, dict):
                raise Exception("Invalid metadata filter condition. Expecting dict instead of {}".format(item))
            subconditions = []
            for k,v in item.items():
                if k not in allowed_fields:
                    raise Exception("Invalid metadata filter field")
                for c in restricted_chars:
                    if c in str(v):
                        raise Exception("Invalid metadata filter value")
                if isinstance(v, str):
                   subconditions.append("{} like %s".format(k))
                else:
                   subconditions.append("{} = %s".format(k))
                params += (v,)
            metadata_conditions.append(" AND ".join(subconditions))
    metacondition_str = " AND (" + " OR ".join(metadata_conditions) + ")" if len(metadata_conditions) > 0 else ""

    data = execute_select_query("""SELECT im.image_id, im.image_name, ex.type_id, im.annotation, im.metadata FROM image_log il 
    LEFT JOIN image_metadata im ON il.image_id = im.image_id 
    LEFT JOIN Execution ex ON ex.id = il.execution_id
    WHERE il.version_id = %s {}
    ORDER BY il.id desc""".format(metacondition_str), params)
    return [{"image_id": item[0], "image_name": item[1], "execution_id": item[2], "annotation": item[3], "metadata": item[4]} for item in data]

def get_image_by_dataset(dataset_id):
    return execute_select_query("SELECT * FROM image_metadata where dataset_id = %s", (dataset_id,))

def get_tenant_id(tenant_name):
    r = execute_select_query("SELECT id FROM tenant where tenant_name = %s", (tenant_name,))
    if len(r) > 0:
      return r[0][0]
    return None

def get_all_tenants():
    r = execute_select_query("SELECT tenant_name, id FROM tenant", None)
    if len(r) > 0:
      return {item[0]:item[1] for item in r}
    return None

def get_model_info_by_dataset(datasetname):
    import json
    r = execute_select_query("SELECT id, model_name, model_type, training_queue, training_dataset, metadata_filter FROM model_info where training_dataset = %s", (datasetname,))    
    return [{"id":item[0], "model_name": item[1], "model_type": item[2], "training_queue":item[3], "metadata_filter":json.loads(item[5]) if item[5] is not None else None} for item in r]

def get_image_metadata(image_names, dataset_id):
    global connection
    ensure_connection()
    dbcursor = connection.cursor()
    temp_table_name = "_" + str(uuid.uuid1()).replace("-", "")
    dbcursor.execute("CREATE TEMPORARY TABLE IF NOT EXISTS {} (_name VARCHAR(300) PRIMARY KEY);".format(temp_table_name))
    dbcursor.executemany("INSERT INTO {}(_name) VALUES (%s);".format(temp_table_name), image_names)
    connection.commit()
    dbcursor.execute("SELECT m.* FROM image_metadata m RIGHT JOIN {} t ON m.image_name=t._name WHERE dataset_id=%s".format(temp_table_name), (dataset_id,))
    r = dbcursor.fetchall()
    return r

def get_annotation_stats(dataset_id):
    r = execute_select_query("SELECT COUNT(image_id), annotation from image_metadata where dataset_id=%s group by annotation", (dataset_id,))
    return {item[1]:item[0] for item in r}

def get_training_history(dataset_name):
    r = execute_select_query("SELECT id, version_id,model_name,exe_status,created_at,updated_at,executed_by FROM training_execution WHERE dataset_name=%s", (dataset_name,))
    return [{"id": item[0], "dataset_version": item[1],"model_name": item[2], "status":item[3],
                "created_at": item[4], "updated_at":item[5], "executed_by":item[6]} for item in r]
