import io
import os
import logging
import pandas as pd
from kflow import authn
from typing import Optional
from dateutil.tz import tzutc
from sqlalchemy import create_engine
from botocore.exceptions import ClientError
from datetime import datetime, timezone, timedelta


### - - - - - -  From Lake



def LakeFileAsObject(path:str, filename:str, bucket:str="klog-lake", **kwargs) -> dict:
    
    """Returns an dict with boto3 format given a path and filename at S3.

    Note
    ----
        TODO: We should standarize the path / filename arguments to URI S3

    Parameters
    ----------
    path: str
        Path after the S3 bucket. Ends in /, starts without /.
    filename: str
        File to load in S3
    bucket: str
        S3 bucket of the path and filename. Default klog-lake.
    **kwargs:
        Keyword arguments are forwarded to the get_object function.

    Returns
    -------
    dict
        Object with information about the file.
        See https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3.html#S3.Client.get_object
    """
    
    s3_client = authn.awsClient()
    s3_bucket = bucket
    s3_path = path
    s3_filename = filename
    s3_key = s3_path + s3_filename
    
    try:
        return s3_client.get_object(Bucket=s3_bucket, Key=s3_key, **kwargs)
    except ClientError as ex:
        if ex.response['Error']['Code'] == 'NoSuchKey':
            logging.warning(f'No object found - returning empty object: {path}{filename}')
            return {}
        else:
            raise

def LakeFileAsDataFrame(path:str, filename:str, bucket:str="klog-lake", format:str="parquet", sheet_name:str=None, **kwargs) -> pd.DataFrame:
    
    """Returns a Dataframe given a path and filename at S3.

    Note
    ----
        TODO: 
        We should standarize the path / filename arguments to URI S3
        Elegir a dónde se rederigen los kwargs, o a las funciones de pandas o a LakeFileAsObject.

    Parameters
    ----------
    path: str
        Path after the S3 bucket. Ends in /, starts without /.
    filename: str
        File to load in S3
    bucket: str
        S3 bucket of the path and filename. Default klog-lake.
    format: str
        Fileformat. Possible values are
        "parquet": parquet, read by pandas directly with pyarrow.
        "xlsx" Excel, read by pandas with default engine.
        "csv" Comma separated textfile. If separated with other caracther, please specific it in kwargs
    **kwargs:
        Keyword arguments are forwarded to the file read function, and can thus specify
        separators or other relevant arguments.        
            compression:str            
            Read compression files set to one of 'zip', 'gzip', 'bz2', 'zstd'
            sep:str
            Define type separator set to one of ',', ';','|'

    Returns
    -------
    pandas.Dataframe
    """
    sep=kwargs.pop("sep",",")
    compression=kwargs.pop("compression",None)

    obj = LakeFileAsObject(path, filename, bucket, **kwargs)
    
    if not obj: # retorna verdadero si el diccionaro está vacío
        return pd.DataFrame()
    if format not in ["parquet","xlsx","csv"]:
        logging.error("Format is not recognized")
        raise
    if format == "parquet":
        return pd.read_parquet(io.BytesIO(obj['Body'].read()), engine='fastparquet', **kwargs)
    elif format == "xlsx":
        return pd.read_excel(io.BytesIO(obj['Body'].read()), sheet_name=sheet_name, **kwargs)
    elif format == "csv":
        return pd.read_csv(io.BytesIO(obj['Body'].read()), keep_default_na=False,sep=sep,compression=compression,**kwargs)

def PrismaTableSnapshot(table:str, date:datetime, detail:bool=False, time_delta=timedelta(days=1)) -> pd.DataFrame:
    
    """Returns a snapshot of a table in prisma, saved in lake, given the table name and date.

    Parameters
    ----------
    table: str
        Name of the table as in the source database.
    date: datetime
        Datetime of the snapshot, timezone aware!
    detail: bool
        Return object, with DataFrame and information about the snapshot loaded
    daily: bool
        If to read snapshots generated daily

    Returns
    -------
    pandas.DataFrame
        Dataframe with all info from the table at that date. Returns an empty DataFrame if not found.

    TODO: Debería mejorarse el caso del detail. Generalizarlo también para snapshots que no sean de Prisma.
    """

    if time_delta.days == 1:
        s = time_delta.total_seconds()
        hours, remainder = divmod(s, 3600)
        minutes, seconds = divmod(remainder, 60)
        snapshot_suffix = f'snapshot-d{int(hours)}_{int(minutes)}'
        date = date.replace(hour=0)
    else:
        s = time_delta.total_seconds()
        hours, remainder = divmod(s, 3600)
        minutes, seconds = divmod(remainder, 60)
        snapshot_suffix = f'snapshot-d{int(hours)}_{int(minutes)}'

    # Check if date is before first snapshot:
    #   1       2       3
    #       LOAD

    if date < date_first_table_snapshot(table) and (date - date_first_table_snapshot(table)).total_seconds() < -(time_delta.total_seconds()):
        if detail:
            return {table:pd.DataFrame(), "table_name":table, "is_initial":False, "is_before_first":True, "expected_not_found":False}
        else:
            logging.warning(f"Table {table}. Date for snapshot before first load - returning empty Dataframe: {date} / {date_first_table_snapshot(table)}")
            return pd.DataFrame()
            
    last_snapshot_filename = f'{date.astimezone(timezone.utc).strftime("%Y%m%d-%H%M%S")}-{snapshot_suffix}.parquet'
    table_snapshot = LakeFileAsDataFrame(f"raw/klog-co-prod/public/{table}/",last_snapshot_filename)
    
    if not table_snapshot.empty:
        # Encontró el archivo, devolver el DataFrame.
        logging.info(f"Table {table}: Load snapshot {last_snapshot_filename}")
        if detail:
            return {table:table_snapshot, "table_name":table, "is_initial":False, "is_before_first":False, "expected_not_found":False}
        else:
            return table_snapshot
    else:
        # If the date is of the initial Snapshot then load the initial Snapshot.
        # Equality between datetimes doesn't work, so we calculate difference in seconds.
        if not time_delta.days == 1:
            date_compare_str_format = '%Y-%m-%d-%H'
        else:
            date_compare_str_format = '%Y-%m-%d'
        
        # Checkin if date is of first snapshot
        if date.astimezone(timezone.utc).strftime(date_compare_str_format) == date_first_table_snapshot(table).astimezone(timezone.utc).strftime(date_compare_str_format):
            logging.info(f"Table {table}: Reading initial snapshot LOAD00000001.parquet")
            table_snapshot = LakeFileAsDataFrame(f"raw/klog-co-prod/public/{table}/","LOAD00000001.parquet")
            if detail:
                return {table:table_snapshot, "table_name":table, "is_initial":True, "is_before_first": False, "expected_not_found":False}
            else:
                return table_snapshot
        else:
            logging.warning(f"Table {table}: Snapshot not found - returning empty Dataframe")
            if detail:
                return {table:pd.DataFrame(), "table_name":table, "is_initial":False, "is_before_first": False, "expected_not_found":True}
            else:
                return pd.DataFrame()

def WarehouseTableSnapshot(table:str , date:datetime, filename:str = None, format:str="csv", time_delta=timedelta(days=1), **kwargs) -> pd.DataFrame:
    
    """
    Returns a snapshot of a table staged for warehouse, saved in lake, given the table name and date.

    Parameters
    ----------
    table: str
        Name of the table as in the warehouse database.
    date: datetime
        Datetime of the snapshot, timezone aware!
    filename: str
        If filename is specified, date is ignored
    format: str
        Format of the file, we pass it explicitly.

    Returns
    -------
    pandas.Dataframe
        Dataframe with all info from the table at that date. Returns an empty DataFrame if not found.

    TODO: Checkear que parámetro format está dentro de los permitidos (csv, parquet)
    """
    if time_delta.days == 1:
        date = date.replace(hour=0)
    if filename == None:
        last_snapshot_filename = f'{date.astimezone(timezone.utc).strftime("%Y%m%d-%H%M%S")}-snapshot.{format}'
    else:
        last_snapshot_filename = filename
    logging.info(f"Warehouse Table {table}: Reading snapshot {last_snapshot_filename}")
    
    if format == "csv":
        # TODO Esto debería estar advertido
        kwargs["sep"] = "|"

    table_snapshot = LakeFileAsDataFrame(f"staging/warehouse/{table}/",last_snapshot_filename, format=format, **kwargs)
    
    if not table_snapshot.empty:
        return table_snapshot
    else:
        logging.warning(f"Warehouse Table {table}: Snapshot not found - returning empty DataFrame")
        return pd.DataFrame()

def LakeFileAsJson(path:str, filename:str, bucket:str="klog-lake") -> dict:
    
    """
    Read a json file from DataLake on S3    
    ----------
    Parameters
    path: str
        Path after the S3 bucket. Ends in /, starts without /.
    filename: str
        File to extract from S3
    bucket: str
        S3 bucket of the path and filename. Default klog-lake.
    ----------
    return
        dicct from json file
    """
    
    import json

    s3_client = authn.awsClient()
    s3_bucket = bucket
    s3_path = path
    s3_filename = filename
    s3_key = s3_path + s3_filename

    try:
        obj = s3_client.get_object(Bucket=s3_bucket, Key=s3_key)
        file_content = obj['Body'].read().decode('utf-8')
    except s3_client.exceptions.NoSuchKey as e:
        logging.warning(f"File not found in S3: {s3_key}. Returning empty dict.")
        return {}
    # TODO Esto debería estar en try, para atrapar errores de parseo.
    return json.loads(file_content)



### - - - - - -  From Prisma



def PrismaTableAsDataFrame(table:str,columns:str="*",where:list=None,schema:str="public",base_env:str='PrismaProd'):    #Old KLogProdTableAsDataFrame
    
    """  
    Return table hosted on Prisma 

    Parameters
    ----------
    table: str
        Name of the table in the Warehouse or Warehosue                 
    columns:str="*"
        Get specific columns. Default all columns!          
    schema:str="public"
        Schema from is hosted warehouse table. Default 'public'         
    base_env:str='PrismaProd'
        "PrismaProd" - Productive enviroment on RDS
    Returns
    -------
    pd.DataFrame
        Prisma table convert to pd.DataFrame
    """

    logging.info(f"Warehouse table as DataFrame: {table}")
    
    prisma_engine = authn.getConnectionDB(base_env)    
    
    if where == None:   
        select_prisma_table = f"""
            SELECT {columns}
            FROM "{schema}"."{table}"
            """
    else:
        select_prisma_table = f"""
            SELECT {columns}
            FROM "{schema}"."{table}"
            WHERE {where[0]}{where[1]}{where[2]}
            """
    
    return pd.read_sql_query(select_prisma_table, prisma_engine)



### - - - - - -  From Warehouse



def WarehouseTableAsDataFrame(table:str,columns:str="*",where:list=None,schema:str="public",base_env:str='WarehouseProd') -> pd.DataFrame:

    """ 
    Return table hosted on Warehouse 

    Parameters
    ----------
    table: str
        Name of the table in the Warehouse or Warehosue               
    columns:str="*"
        Get specific columns. Default all columns!         
    schema:str="public"
        schema from is hosted warehouse table. Default 'public'          
    base_env:str='WarehouseProd'
        "WarehouseProd" - Productive enviroment on Redshift        
    Returns
    -------
    pd.DataFrame
        Warehouse table convert to pd.DataFrame
    """

    logging.info(f"Warehouse table as DataFrame: {table}")
    
    warehouse_engine = authn.getConnectionDB(base_env) 
    if where == None:   
        select_wh_table = f"""
            SELECT {columns}
            FROM "{schema}"."{table}"
            """
    else:
        select_wh_table = f"""
            SELECT {columns}
            FROM "{schema}"."{table}"
            WHERE {where[0]}{where[1]}{where[2]}
            """

    return pd.read_sql_query(select_wh_table, warehouse_engine)

def WarehouseTableLastLoad(table:str,bucket:str="klog-lake") -> datetime:
    
    """Devuelve fecha de la última carga de una tabla al warehouse.
    TODO No se usa. Borrar?
    """

    s3_client = authn.awsClient()
    table_staging_load_files = s3_client.list_objects_v2(Bucket=bucket, Prefix=f'staging/warehouse/{table}/')
    table_staging_load_files = sorted(table_staging_load_files["Contents"], key=lambda x: x["LastModified"])
    return table_staging_load_files[-1]["LastModified"]

def WarehouseTableOperations(table:str,initial_date=datetime(2000,1,1,00,00,00, tzinfo=tzutc()),last_date=datetime(3000, 1, 1, 00, 00, 00, tzinfo=tzutc()),
                            bucket:str="klog-lake",db:str="klog-co-prod",schema:str="public",with_date:bool=False):
    
    """
    Given a table, returns Dataframe were each row is an operation realized on the table after the given date.
    TODO Documentar argumentos.
    TODO Esta función está asumiendo que los snapshots son de cada día.
    """

    s3_client = authn.awsClient()
    
    table_operation_objects = s3_client.list_objects_v2(Bucket=bucket, Prefix=f'raw/{db}/{schema}/{table}/{(initial_date.strftime("%Y%m%d"))}')
    if "KeyCount" in table_operation_objects.keys():
        if table_operation_objects["KeyCount"] == 0:
            logging.info("No files found, returning empty DataFrame")
            return pd.DataFrame()
    table_operation_files = table_operation_objects["Contents"]
    table_operation_objects = s3_client.list_objects_v2(Bucket=bucket, Prefix=f'raw/{db}/{schema}/{table}/{((initial_date + timedelta(days=1)).strftime("%Y%m%d"))}')
    if "Contents" in table_operation_objects.keys():
        table_operation_files += table_operation_objects["Contents"]
    # Sort by last modified. Important so that returned dataframe is properly ordered
    table_operation_files = sorted(table_operation_files, key=lambda x: x["LastModified"])
    # Filter files later than specified date
    if last_date == None:
        last_date = datetime(3000, 1, 1, 00, 00, 00, tzinfo=tzutc())
    table_operation_files = list(filter(lambda x: (x["LastModified"] > initial_date)&(x["LastModified"] <= last_date), table_operation_files))
    # Remove LOAD files
    table_operation_files = list(filter(lambda x: x["Key"].find("LOAD") == -1, table_operation_files))
    # Remove SNAPSHOTS
    table_operation_files = list(filter(lambda x: x["Key"].find("snapshot") == -1, table_operation_files))
    dfs = []
    for file in table_operation_files:
        #logging.info(f"Downloading file {file}")
        df = LakeFileAsDataFrame(os.path.dirname(file["Key"])+"/",os.path.basename(file["Key"]))
        if with_date:
            df["file_date"] = file["LastModified"]
        dfs.append(df)
    if len(dfs) != 0:
        return pd.concat(dfs)
    else:
        return pd.DataFrame()


### - - - - - -  From Google Sheets



def GoogleSheetsToList(sheet_id:str, sheet_range:str, auth="SERVICE"):
    """Returns the data in a Google Sheet as a list
    
    Parameters
    ----------
    sheet_id: str
        ID of the Google Sheet, as found on the Sheet url.
    sheet_range: str
        Range of values to take, using A1 notation. Must include Sheet name.
    auth: str
        Authentication type, see authn.getConnectionGoogleSheet

    Returns
    -------
    list
        List with all info from the Google Sheet range specified.
    TODO Revisar si se puede devolver lista vacía cuando no encuentra datos.
    TODO El try para el HttpError podría sacarse.
    """

    from kflow import load
    from googleapiclient.errors import HttpError

    try:
        service = authn.getConnectionGoogleSheet(auth=auth)
        sheet = service.spreadsheets()
        # valueRenderOption devuelve valor sin formato (por ejemplo, si en el Sheet sale $15.0, devuelve 15.0, no "$15.0")
        # Ojo que esto hace que las fechas se devuelvan como int. (12312351231, Epoch de Google)
        result = sheet.values().get(spreadsheetId=sheet_id, range=sheet_range, valueRenderOption='UNFORMATTED_VALUE').execute()
        values = result.get('values', [])
        if not values:
            logging.error('No data found.')
            return
        return values

    except HttpError as err:
        logging.error(err)

def GoogleSheetsToDataFrame(*args, **kwargs):
    """Takes a Google Sheets and returns a DataFrame.

    Uses GoogleSheetsToList, and transforms list to DataFrame.
    TODO Lo de la primera fila y la primera columna deberían ser opciones
    """
    list = GoogleSheetsToList(*args, **kwargs)
    df = pd.DataFrame(list)
    if df.empty:
        logging.warning("Returning empty dataframe")
        return df
    # Columnas toman el nombre de la primera fila.
    df.columns = df.iloc[0]
    # Bota columna de índice
    df = df.drop(0)
    return df



### - - - - - -  From Hubspot

def _HubspotLoopSearch(type_object,filter_date,properties_list,client):

    """
    Documentar
    """
    
    from time import sleep    
    from hubspot.crm.companies import PublicObjectSearchRequest, ApiException

    if type_object == 'companies':        
        api_response = client.crm.companies.search_api.do_search(PublicObjectSearchRequest(filter_groups=[{"filters":filter_date}]))
    elif type_object == 'contacts':
        api_response = client.crm.contacts.search_api.do_search(PublicObjectSearchRequest(filter_groups=[{"filters":filter_date}]))

    total_companies = api_response.to_dict()['total']
            
    n_after=0    
    list_date_range = []

    while n_after < total_companies:     

        public_object_search_request = PublicObjectSearchRequest(properties=properties_list,
                                                                 limit=100,
                                                                 after=n_after,
                                                                 filter_groups=[{"filters":filter_date}])
        try:

            if type_object == 'companies':            
                api_response = client.crm.companies.search_api.do_search(public_object_search_request=public_object_search_request)
            
            elif type_object == 'contacts':
                api_response = client.crm.contacts.search_api.do_search(public_object_search_request=public_object_search_request)   

        except ApiException:
            raise
        
        dict_response = api_response.to_dict()['results']
        list_dict = [value['properties'] for value in dict_response]
        list_date_range = list_date_range + list_dict 

        n_after+=100        
        sleep(1)
                    
    return list_date_range 


def HubspotToDataFrame(type_object:str,fields_list:list=None,hubspot_env:str="HubspotProd") -> pd.DataFrame:  #Old HubspotComapaniesToDataFrame
    
    """
    Read Companies table from Hubspot

    **Install hubspot library >> pip install hubspot-api-client

    Parameters
    --------------------
    fields_list:list
        Fields of companies object on Hubspot   
    hubspot_env:str="HubspotProd"        
        HubspotProd - ambiente productivo
        HubspotTest - ambiente de pruebas
    --------------------
    Return
        Dataframe with Hubspot's Companies
    """
 
    import hubspot   
    from time import sleep 
    from hubspot.crm.companies import PublicObjectSearchRequest, ApiException

    if type_object == 'companies':

        properties = ['id_natural','name','tax_id','lifecyclestage','hubspot_owner_id',
                    'num_associated_deals','hubspot_owner_assigneddate','klog_country','tier']
    
    elif type_object == 'contacts':
        
        properties = ['name','email','hs_object_id','hs_created_by_user_id','company','hubspot_owner_id',
                      'hubspot_owner_assigneddate','createdate','hs_created_by_user_id','lifecyclestage']
     
    if fields_list == None:
        properties_list = properties
    else:
        properties_list = properties + fields_list 
        properties_list = list(set(properties_list))

    date_range = LakeFileAsJson("json-files/","hubspot_data_range.json","klog-etl")
    client = authn.getHubspotClient(hubspot_env)    
    
    data_concat = []

    for i in range(len(date_range)-1):
        
        date = list(date_range.values())        
        filter_date = [{"propertyName":"createdate","operator":"BETWEEN","value":f"{date[i]}","highValue":f"{date[i+1]}"}]
        df_hub_range = _HubspotLoopSearch(type_object,filter_date,properties_list,client)
        data_concat.extend(df_hub_range)     

    df_hub_final = pd.DataFrame.from_dict(data_concat)       

    logging.info(f"Export {len(df_hub_final)} rows")   

    return df_hub_final

def HubspotOwners(hubspot_env:str="HubspotProd") -> pd.DataFrame:    

    from hubspot.crm.owners import ApiException

    """
    Read Owner table from Hubspot.
     **Install hubspot library >> pip install hubspot-api-client

     Parameters
    --------------------
    fields:list
        Fields of companies object on Hubspot   
    hubspot_env:str="HubspotProd"       
        HubspotProd - ambiente productivo
        HubspotTest - ambiente de pruebas
    --------------------
    Return
        Dataframe with Hubspot's owner
    """ 
    client = authn.getHubspotClient(hubspot_env)

    try:
        api_response = client.crm.owners.owners_api.get_page(limit=100,archived=False)                                                                    
    except ApiException:
        raise

    list_response = api_response.to_dict()['results'] 
    df_owners = pd.DataFrame.from_dict(list_response)   
 
    df_owners['teams'] = [None if i == None else i[0]['name'] for i in df_owners['teams']]
    df_owners['user_id'] = df_owners['user_id'].astype(int).astype(str)

    return df_owners


### - - - - - -  From SQL query (sql hosted on S3)


def SQLFileToString(path:str, filename:str, bucket:str="klog-etl")-> str:

    """
    DOCUMENTAR
    """

    obj = LakeFileAsObject(path, filename, bucket)

    sql_file = obj['Body'].read().decode('utf-8')

    return sql_file

def SQLFileToDataframe(path:str, sql_filename:str, base_env:str, template_params=None, bucket:str="klog-etl"): 
    
    """  
    Documentar
    """

    bd_engine = authn.getConnectionDB(base_env)

    query = SQLFileToString(path,sql_filename,bucket)

    params = ()
    if template_params:
        from jinjasql import JinjaSql
        j = JinjaSql()
        query, bind_params = j.prepare_query(query, template_params)
    else:
        query = query.replace("%","%%")
        bind_params = None
    
    return pd.read_sql_query(query, bd_engine, params=bind_params)



### - - - - - - Manager SQS

def receive_queue_message(queue_url):
    """
    Retrieves one or more messages (up to 10), from the specified queue.
    """
    sqs_client = authn.awsClient(service='sqs')
    
    try:
        messages = sqs_client.receive_message(QueueUrl=queue_url,
                                              MaxNumberOfMessages=10,
                                              WaitTimeSeconds=10,
                                              MessageAttributeNames=['All'])
    except ClientError:
        logging.exception(
            f'Could not receive the message from the - {queue_url}.')
        raise
    else:             
        return messages


### - - - - - -  From ??


def date_first_table_snapshot(table:str):
    
    """Gets the first dump of a database table.

    This is useful to know when did CDC start for each table and thus for the generation of snapshots and others.
    """

    initial_snapshot_obj = LakeFileAsObject(f"raw/klog-co-prod/public/{table}/","LOAD00000001.parquet")
    if "lastmodified" in initial_snapshot_obj["Metadata"].keys():
        return datetime.fromisoformat(initial_snapshot_obj["Metadata"]["lastmodified"]).astimezone(timezone.utc)
    else:
        return initial_snapshot_obj["LastModified"]

def PrismaTablesInLake():
    
    """
    Returns all prisma tables which are being stored at Lake. This info is stored in meta_prisma_tables in the warehouse.
    """
    return WarehouseTableAsDataFrame("meta_prisma_tables")


