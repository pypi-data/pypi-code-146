import logging
import sqlalchemy 
import pandas as pd
from smart_open import open
from kflow import extract,authn
from datetime import datetime, timezone



### - - - - - -  To Lake

def DataFrameToLake(path:str, filename:str, df:pd.DataFrame, bucket:str="klog-lake", format:str="parquet"):
    """
    Sends a DataFrame to S3, in different file formats.

    It uses smart_open open function. This requires the correct credentials,
    looked for at the .aws directory at local.

    Parameters
    ----------
    path: str
        Path after the S3 bucket. Ends in /, starts without /.
    filename: str
        File to create in S3
    df:
        DataFrame to save
    bucket: str
        S3 bucket of the path and filename. Default 'klog-lake'.
    format:
        'parquet' or 'csv'. Default 'parquet'
    """


    session = authn.awsClient(type_auth='session')
    s3_output = f's3://{bucket}/{path}/{filename}'
    with open(s3_output, 'wb', transport_params={'client': session.client('s3')}) as out_file:
        if format == "parquet":
            # Arguments of timestamps are used to avoid type conflict when reading timestamps with higher precision
            # This is a known issue of S3 storage, pyarrow and Pandas.
            df.to_parquet(out_file, engine='pyarrow', index=False, allow_truncated_timestamps=True, coerce_timestamps ='ms')
        elif format == "excel":
            df.to_excel(out_file, index=False)
        elif format == "csv":
            # TODO Separador está hardcodeado
            df.to_csv(out_file, index=False, sep="|")

def JsonToLake(path, filename, json, bucket='klog-lake'):
    
    """
    Load a json file to DataLake on S3
    ----------
    Parameters
    path: str
        Path after the S3 bucket. Ends in /, starts without /.
    filename: str
        File to load S3
    bucket: str
        S3 bucket of the path and filename. Default klog-lake.
    ----------
    """

    s3_key = f'{path}/{filename}'
    s3_client = authn.awsClient()
    s3_client.put_object(Body=json, Bucket=bucket,Key=s3_key)

def GoogleSheetsToLake(path:str, sheet_id:str, sheet_range:str, sheet_name:str, date=None, **kwargs):
    
    """
    Loads a Google Sheets' Sheet to the lake

    Parameters
    ----------
    path: str
        Path after the S3 bucket. Ends without /, starts without /.
    sheet_id: str
        The id of the Sheet. This is part of the url of the sheet, see Google doc.
    sheet_range: str
        The range of the sheet to upload, expressed in A1 format.
    sheet_name: str
        The name of the sheet (tab, pestaña) to load.
    date: 
        The date, to format the name with a given standard
    """
    sheet = extract.GoogleSheetsToDataFrame(sheet_id, sheet_range, sheet_name=sheet_name, **kwargs)
    filename = f"google_sheet_{sheet_id}_{sheet_name}_{date.strftime('%Y%m%d%H%M%S')}"
    DataFrameToLake(path, filename, sheet, format="parquet") 

def SnapshotWarehouseToDataLake(table:str,date:datetime,schema:str="public",bucket_data_lake:str="klog-lake",format_file:str="parquet") -> pd.DataFrame:

    """Create snapshot on DataLake from a Warehouse table.

    **Check dependencies to WarehouseTableAsDataFrame() and DataFrameToLake()

    Parameters
    --------------------
    table:str
        Name of the table as in the warehouse database.
    date:datetime
        Datetime of the snapshot, timezone aware!
    schema
        schema from is hosted warehouse table. Default 'public'       
    bucket_data_lake
        Buckets on Datalake where will hosted snapshot. Default 'klog-lake'
    format_file
        'parquet' or 'csv'. Default 'parquet'
    --------------------
    """

    WarehouseTable = extract.WarehouseTableAsDataFrame(table,schema)

    filename = f'{date.astimezone(timezone.utc).strftime("%Y%m%d-%H%M%S")}-snapshot.{format_file}'

    DataFrameToLake(f'staging/warehouse/{table}',filename, WarehouseTable,bucket_data_lake,format_file)

    return WarehouseTable

def SnapshotDataFrameToDataLake(df:pd.DataFrame,date:datetime,path:str,bucket_data_lake:str="klog-lake",format_file:str="parquet") -> pd.DataFrame:

    """Create snapshot on DataLake from a DataFrame.

    **Check dependencies to DataFrameToLake()

    Parameters
    --------------------
    df:pd.DataFrame
        Pandas DataFrame to send DataLake.
    date:datetime
        Datetime of the snapshot, timezone aware!
    path:str
        S3 Path where save snapshot, start and end without " / "       
    bucket_data_lake
        Buckets on Datalake where will hosted snapshot. Default 'klog-lake'
    format_file
        'parquet' or 'csv'. Default 'parquet'
    --------------------
    """

    filename = f'{date.astimezone(timezone.utc).strftime("%Y%m%d-%H%M%S")}-snapshot.{format_file}'

    df = DataFrameToLake(f'{path}',filename, df, bucket_data_lake, format_file)

    return df   

def QueryToDataLake(path:str,sql_filename:str,uri_s3:str,sep:str='|',repo:str="teu-ai/etl",base_env:str='WarehouseProd'):

    """Create file on Data Lake from sql query

    **Install GitHub library >> pip install PyGithub

    Parameters
    --------------------
    sql_file:str
        Sql file's path on Github repo. e.g "sql/querys/Select_operation_billed.sql"
    uri_s3:str
        Data Lake path to send data file, include namefile e.g 's3://klog-lake/staging/warehouse/fact_operation_billed/fact_operation_billed_20220912'
    repo:str="teu-ai/etl"
        Repository where hosted sql files    
    """

    warehouse_engine = authn.getConnectionDB(base_env)
    role_S3ToRedshift = authn.getIAMRole("dms-access-for-endpoint")

    query = extract.SQLFileToString(path,sql_filename)       

    sql = f"""
        UNLOAD ('{query}')
        TO '{uri_s3}'
        CREDENTIALS 'aws_iam_role={role_S3ToRedshift}'
        PARALLEL OFF
        ALLOWOVERWRITE
        DELIMITER '{sep}'
        HEADER
        zstd;
        """

    warehouse_engine.execute(sql) 



### - - - - - -  To Warehouse


def map_pandera_schema_to_sqlalchemy_types(schema):
    # Maps Pandera schema to SQLAlchemy types, used for DataFrame.to_sql dtypes argument.
    # MetaSchema exists to check equality of types.
    import pandera as pa
    from sqlalchemy.types import VARCHAR, TIMESTAMP, FLOAT, INTEGER
    meta_schema = pa.DataFrameSchema({
        "str": pa.Column(str, pa.Check.str_length(max_value=256)),
        "float": pa.Column(float),
        "int": pa.Column(int),
        "timestamp": pa.Column(datetime)
    })
    def pandera_to_sqlalchemy(type_pandera, checks):
        # The actual map, checks are used for VARCHAR lengths.
        if type_pandera == meta_schema.columns["str"].dtype:
            if len(checks):
                return VARCHAR([check._statistics["max_value"] for check in checks if check.name == "str_length"][0])
            else:
                return VARCHAR(256)
        elif type_pandera == meta_schema.columns["float"].dtype:
            return FLOAT
        elif type_pandera == meta_schema.columns["int"].dtype:
            return INTEGER
        elif type_pandera == meta_schema.columns["timestamp"].dtype:
            return TIMESTAMP
        else:
            return VARCHAR(256)
    
    return {a:pandera_to_sqlalchemy(b,schema.columns[a].checks) for (a,b) in schema.dtypes.items()}


def DataFrameToWarehouse(table:str,
                         df:pd.DataFrame,
                         dtype:dict = None,
                         delete_table:bool = True,                         
                         base_env:str ='WarehouseProd',
                         to_lake_args = None,
                         to_sql_kwargs = {"index":False, 'if_exists':'append', 'schema':'public', "method":'multi','chunksize':5000}
                        ):
    
    """
    Uploads DataFrame directly to warehouse, by creating or appending to table.

    IMPORTANT: default this function clean all table (sql drop) and after append your new rows.
    if yor table is not or you replace is table, this table create with sql default type format and
    it's posiible that you have problem with field lengh por example.

    Parameters
    ----------
    table: str
        Name of the table in the Warehouse.
    df: pd.DataFrame
        DataFrame to upload.
    delete_table:bool=True
        If 'true', then the table is deleted of data before inserting new data.
    if_exists:str='append'
        'replace', 'fail', 'append', see to_sql method documentation.    
    base_env:str='WarehouseProd'
        "WarehouseProd" - Productive enviroment on Redshift 
    """

    warehouse_engine = authn.getConnectionDB(base_env)

    if to_lake_args:
        DataFrameToLake(*to_lake_args)

    if delete_table:
        schema = to_sql_kwargs["schema"] if "schema" in to_sql_kwargs.keys() else "public"
        WarehouseDeleteTable(table, schema=schema, warehouse_engine=warehouse_engine)
    try:
        df.to_sql(table, warehouse_engine, dtype=dtype, **to_sql_kwargs)
    except Exception as e:

        # Se trunca el mensaje de error, porque cuando uno inserta muchísimas filas,
        # en el error devuelve todas las filas, entonces el mensaje puede ser muy grande,
        # y en ese caso MWAA se cae (no se puede ver el log en AWS).
        # TODO Encontrar una mejor forma de manejarlo
        
        msg = str(e)
        print(f"error en to_sql:{msg[0:1000]}")
        exit(1)

def lake_parquet_to_warehouse(filename,table:str,schema:str='public',bucket="klog-lake",base_env:str='WarehouseProd'):
    
    """
    TODO Documentar
    TODO La opción de borrar la tabla debería venir como argumento.
    """
    warehouse_engine = authn.getConnectionDB(base_env)
    role_S3ToRedshift = authn.getIAMRole("RedshiftSpectrum")
    filepath = f's3://{bucket}/staging/warehouse/{table}/{filename}'
    logging.info("Deleting table")
    sql = f"""
        delete {schema}.{table};
        copy {schema}.{table}
        from '{filepath}'
        iam_role '{role_S3ToRedshift}'
        format as parquet;
        """
    return warehouse_engine.execute(sql)

def LakeToWarehouse(filename,
                    table:str,
                    columns=[],
                    schema:str='public',
                    bucket="klog-lake",
                    from_dataframe=False,
                    from_dataframe_kwargs={"format":"csv", "sep":"|"},
                    to_sql_kwargs={"index":False,'if_exists':'append','schema':'public', "method":'multi','chunksize':5000},
                    dtype:dict = None,
                    postgres=False,
                    delete_table=True,
                    base_env:str='WarehouseProd'):
    
    """
    Loads a DataFrame saved in the Lake to the Warehouse.
    TODO These function should be separated in two.
    TODO Esta función debería ser solo el último caso donde lee un csv, y se debería llamar LakeCsvToWarehouse.
    """

    warehouse_engine = authn.getConnectionDB(base_env)
    if not from_dataframe:
        if len(columns) > 0:
            columns_str = ['"'+str(x)+'"' for x in columns]
            columns_formated = f'({", ".join(columns_str)})'
        else:
            columns_formated = ""
        filepath = f's3://{bucket}/staging/warehouse/{table}/{filename}'
        if not postgres:
            role_S3ToRedshift = authn.getIAMRole("RedshiftSpectrum")
            sql = f"""
                delete {schema}.{table};
                copy {schema}.{table} {columns_formated}
                from '{filepath}'
                iam_role '{role_S3ToRedshift}'
                delimiter '|'
                ignoreheader 1
                EMPTYASNULL;
                """
        else:
            sql = f"""
                drop table {schema}.{table};
                copy {schema}.{table} {columns_formated}
                from '{filepath}'
                delimiter '|';
                """
        return warehouse_engine.execute(sql)
    else:
        # We read file as dataframe and insert dataframe to db.
        df = extract.LakeFileAsDataFrame(f"staging/warehouse/{table}/", filename, **from_dataframe_kwargs)
        if delete_table:
            WarehouseDeleteTable(table, schema=schema, warehouse_engine=warehouse_engine)
        return df.to_sql(table, warehouse_engine,dtype=dtype,**to_sql_kwargs)

def WarehouseUpdateRow(table:str,row:object,schema:str="public",id_column_name:str="id",base_env:str='WarehouseProd'):
    
    """
    Updates a row of a given table in the warehouse given a dictionary with the rows columns.

    Parameters
    ----------
    table: str
        Table in the warehouse to update.
    row: str
        Object with the information of the row. Columns that are not included are not updated.
    schema: str
        Schema in the database
    id_column_name: str
        Name of the column that contains the unique id. If there is no unique id it is not possible to update
    base_env:str='WarehouseProd'
        "WarehouseProd" - Productive enviroment on Redshift
    """

    warehouse_engine = authn.getConnectionDB(base_env)

    update_set = ""
    for column, value in dict(row).items():
        # Values that are None are not added as column-value pairs, that way we manage the
        # DB default values properly
        if value == None:
            continue
        if isinstance(value, str):
            value = value.replace("'","\\'")
        update_set += f"{column} = '{value}', "
    update_set = update_set[0:-2]
    id = row[id_column_name]
    
    sql = f"""
        update "{schema}"."{table}"
        set {update_set}
        where {id_column_name} = '{id}'
        """

    warehouse_engine.execute(sql)

def WarehouseTableExists(table, schema="public", base_env:str='WarehouseProd'):
    
    """
    Returns if a table exists in the warehouse.
    It uses the PostgreSQL view pg_tables

    Parameters
    ----------
    table:str
        Name of the table to check for existence
    schema:str
        The schema where the table is
    base_env:str='WarehouseProd'
        "WarehouseProd" - Productive enviroment on Redshift 
    """

    sql = f"""--sql
        SELECT EXISTS (SELECT * FROM pg_tables WHERE schemaname = '{schema}' AND tablename  = '{table}');
    """    
    warehouse_engine = authn.getConnectionDB(base_env)
    cursor =  warehouse_engine.execute(sql)
    result = cursor.fetchall()
    return result[0][0]

def WarehouseDeleteTable(table, base_env:str='WarehouseProd', schema="public", warehouse_engine=None):
    
    """
    Clears a warehouse table (DELETE SQL statement)

    Parameters
    ----------
    table: str
        Name of the table to clear    
    base_env:str='WarehouseProd'
        "WarehouseProd" - Productive enviroment on Redshift
    warehouse_engine=None
        Instance of SQLAlchemy Engine
    """

    if warehouse_engine == None:
        warehouse_engine = authn.getConnectionDB(base_env)

    if WarehouseTableExists(table, schema=schema):
        sql = f"""
            DELETE FROM {schema}.{table}
            """
        warehouse_engine.execute(sql)
    else:
        logging.warning("Tried to delete table that doesn't exist")

def WarehouseInsertRow(table:str, row:object, schema="public", base_env:str='WarehouseProd'):
    
    """
    Inserts a row in a table

    Parameters
    ----------
    table: str
        Name of the table to clear
    row:
        Dictionary with values to insert to each column (keys).
    schema:
        Schema in the database
    base_env:str='WarehouseProd'
        "WarehouseProd" - Productive enviroment on Redshift 
    """

    warehouse_engine = authn.getConnectionDB(base_env)

    columns = ""
    values = ""

    for column, value in dict(row).items():
        # Values that are None are not added as column-value pairs, that way we manage the
        # DB default values properly
        if value == None:
            continue
        if isinstance(value, str):
            value = value.replace("'","\\'")
        columns += f"{column}, "
        values += f"'{value}', "
    columns = "("+columns[0:-2]+")"
    values = "("+values[0:-2]+")"
    sql = f"""
        insert into "{schema}"."{table}" {columns}
        values {values}
        """

    warehouse_engine.execute(sql)

def LakeCsvToWarehouse(table:str,uri_s3:str,columns=[],schema:str="public",sep:str='|',compress:str=None):

    warehouse_engine = authn.getConnectionDB('WarehouseProd')
    role_S3ToRedshift = authn.getIAMRole("dms-access-for-endpoint")

    if len(columns) > 0:
            columns_str = ['"'+str(x)+'"' for x in columns]
            columns_formated = f'({", ".join(columns_str)})'
    else:
        columns_formated = ""

    if compress ==None:
        end=";"
        compress_end=""
    else:
        end=""
        compress_end=f"{compress};"

    sql = f"""
        delete {schema}.{table};
        copy {schema}.{table} {columns_formated}
        from '{uri_s3}'
        iam_role '{role_S3ToRedshift}'
        delimiter '{sep}'
        ignoreheader 1
        EMPTYASNULL{end}
        {compress_end}
        """

    warehouse_engine.execute(sql)



### - - - - - -  To Google_Sheets



def GoogleSheetsClearSheet(sheet_id:str, sheet_name:str="Sheet1", auth:str="SERVICE"):
    
    """
    Clears a Google Sheet (deletes all values)

    Parameters
    ----------
    sheet_id: str
        The id of the Sheet. This is part of the url of the sheet, see Google doc.
    sheet_name: str
        The name of the sheet (tab, pestaña) to load.
    auth: 
        Type of authentication to use
    auth_key:
        Key for authentication
    """
    service = authn.getConnectionGoogleSheet(auth)
    sheet = service.spreadsheets()
    sheet.values().clear(spreadsheetId=sheet_id, range=f"{sheet_name}").execute()

def DataFrameToGoogleSheet(df:pd.DataFrame,sheet_id:str,update:bool=False,update_key:str="OP",sheet_name:str="Sheet1",auth:str="SERVICE",column_names_row:bool=False) -> pd.DataFrame:
    """
    Loads a DataFrame to a Google Sheets

    Parameters
    ----------
    df:
        DataFrame to upload
    sheet_id: str
        The id of the Sheet. This is part of the url of the sheet, see Google doc.
    update:
        If true, then the current sheet is downloaded and updated based on a merge with the given update_key
    update_key:
        Unique identifier to update each row
    sheet_name: str
        The name of the sheet (tab, pestaña) to load.
    auth: 
        Type of authentication to use
    auth_key:
        Key for authentication
    column_names_row:
        If the first row contains column names

    TODO El try no es necesario
    """
    import os.path

    from googleapiclient.errors import HttpError

    logging.info(f"Writing to Google Sheet: {sheet_id}:{sheet_name}")

    int_to_letter = {1:"A",2:"B",3:"C",4:"D",5:"E",6:"F",7:"G",8:"H",9:"I",10:"J",11:"K",12:"L",13:"M",14:"N",15:"O",16:"P",
        17:"Q",18:"R",19:"S",20:"T",21:"U",22:"V",23:"W",24:"X",25:"Y",26:"Z",27:"AA",28:"AB",29:"AC",30:"AD",31:"AE"}

    try:
        
        service = authn.getConnectionGoogleSheet(auth)

        # Call the Sheets API
        sheet = service.spreadsheets()

        if update:
            # Get current sheet to append other columns
            current = pd.DataFrame(extract.GoogleSheetsToList("1PZbdNT1Rzk5aVxY5wRtz2rFFuQTaTqmW7DfmJYaOx7o",f"{sheet_name}", auth=auth, auth_key=auth_key))
            current = current.rename(columns=current.iloc[0]).drop(current.index[0])
            current = current.loc[:,[x for x in current.columns if x not in df.columns[1:]]]
            if len(current) > 0:
                # Merge all columns to new state
                df = pd.merge(df, current, on=update_key, how="left")
                df = df.fillna("")

        if not column_names_row:
            ri = 2
        else:
            ri = 1
        rf = ri+df.shape[0]
        ci = 1
        cf = ci+df.shape[1]

        if column_names_row:
            df = df.reset_index(drop=True)
            df.loc[-1] = df.columns
            df = df.sort_index()

        result = sheet.values().update(
            spreadsheetId=sheet_id,
            range=f"{sheet_name}!{int_to_letter[ci]}{ri}",#!{int_to_letter[ci]}{ri}:{int_to_letter[cf]}{rf}",
            body={"values":df.values.tolist()},
            valueInputOption="USER_ENTERED").execute()

    except HttpError as err:
        logging.error(err)
    
    return df

def update_column_google_sheets(df:pd.DataFrame,sheet_id:str,range:str):
    
    """
    Función para actualizar una columna de un Sheet

    TODO: No debería existir, basta con actualizar con un Dataframe y especificar una columna de rango.
    """
    service = authn.getConnectionGoogleSheet(auth="SERVICE")
    sheet = service.spreadsheets()
    sheet.values().update(spreadsheetId=sheet_id, range=range, valueInputOption="USER_ENTERED", body={"values":df.values.tolist()}).execute()



### - - - - - -  To Hubspot



def DataFrameCompaniesToHubspot(df:pd.DataFrame,id_field:str,hubspot_env:str="HubspotProd")  -> pd.DataFrame:

    """Send Companies to Hubspot.

    **Install hubspot library >> pip install hubspot-api-client

    Parameters
    --------------------
    df:pd.DataFrame
        DataFrame to send Hubspot. Fields's name to should the same to Hubspot companies
    id_field:str
        ID Field name to recovery hubspot information
    hubspot_env:str="HubspotProd"       
        HubspotProd - ambiente productivo
        HubspotTest - ambiente de pruebas       
    --------------------
    Return
    pd.DataFrame
        The same DataFrame that you send but with some Hubspot fields how id_hubspot, label_owner ect.
    --------------------
    """

    from time import sleep
    from hubspot.crm.companies import BatchInputSimplePublicObjectInput, ApiException

    client = authn.getHubspotClient(hubspot_env) 

    dict_create = df.to_dict(orient='records')

    load_list=[]

    for i in dict_create:
            
        dict_template = {"properties":i}
        load_list.append(dict_template)
            
    batch_input_simple_public_object_input = BatchInputSimplePublicObjectInput(inputs=load_list)

    try:
        api_response = client.crm.companies.batch_api.create(batch_input_simple_public_object_input=batch_input_simple_public_object_input)
            
    except ApiException:
            raise 

    sleep(3)  
    
    df_uplodaded = extract.HubspotCompaniesToDataFrame(list(df.columns),hubspot_env)
    df_uplodaded = df_uplodaded.loc[df_uplodaded[id_field].isin(list(df[id_field]))]  ## pendiente de mejorar con un merge
    
    return df_uplodaded

def _UpdateCompaniesHubspot(df_hub_send:pd.DataFrame,hubspot_env:str="HubspotProd"):

    """Send Updaes (less that 100) to Companies to Hubspot.

    **Install hubspot library >> pip install hubspot-api-client

    Parameters
    --------------------
    df:pd.DataFrame
        DataFrame to send Hubspot. Fields's name to should the same to Hubspot companies
        ****** IMPORTANT: the firts fields must be 'hs_object_id' because it's a key to match update on Hubspot ********
    hubspot_env:str="HubspotProd"        
        HubspotProd - ambiente productivo
        HubspotTest - ambiente de pruebas        
    --------------------
    Return
    API response
    --------------------
    """

    from hubspot.crm.companies import BatchInputSimplePublicObjectBatchInput, ApiException     

    dict_create = df_hub_send.to_dict(orient='records')

    update_list=[]

    for i in dict_create:
        
        dict_filter = lambda x, y: dict([ (i,x[i]) for i in x if i in set(y)])
        large_dict = i
        new_dict_keys = tuple(list(df_hub_send.columns)[1:])
        small_dict=dict_filter(large_dict, new_dict_keys)
                
        dict_template = {"id":i['hs_object_id'],"properties":small_dict}
        update_list.append(dict_template)

    client = authn.getHubspotClient(hubspot_env) 

    batch_input_simple_public_object_batch_input = BatchInputSimplePublicObjectBatchInput(inputs=update_list)

    try:
        api_response = client.crm.companies.batch_api.update(batch_input_simple_public_object_batch_input=batch_input_simple_public_object_batch_input)        
        return api_response
            
    except ApiException:
        raise

def UpdateBatchCompaniesHubspot(df_hub_send:pd.DataFrame,hubspot_env:str="HubspotProd"):

    """Send Updaes (more that 100) to Companies to Hubspot.

    **Install hubspot library >> pip install hubspot-api-client

    Parameters
    --------------------
    df:pd.DataFrame
        DataFrame to send Hubspot. Fields's name to should the same to Hubspot companies
        ****** IMPORTANT: the firts fields must be 'hs_object_id' because it's a key to match update on Hubspot ********
    hubspot_env:str="HubspotProd"        
        HubspotProd - ambiente productivo
        HubspotTest - ambiente de pruebas       
    --------------------
    Return
    API response
    --------------------
    """

    import math

    top = len(df_hub_send)
    last_iteration = math.ceil(len(df_hub_send)/100)-1
    count_iteration = 0    

    for i in range(0,top,100):

        if count_iteration < last_iteration:
                
            update_df = df_hub_send.iloc[i:i+99,:]
            _UpdateCompaniesHubspot(update_df,hubspot_env)      
            count_iteration += 1

        else:
            update_df = df_hub_send.iloc[i:,:]
            _UpdateCompaniesHubspot(update_df,hubspot_env)
          
def send_queue_message(queue_url, payload, **kwargs):
    """
    Sends one messages to the specified queue.
    """
    sqs_client = authn.awsClient(service='sqs')
    
    try:
        response = sqs_client.send_message(
            QueueUrl=queue_url,
            MessageBody=payload,
            **kwargs
        )
    except ClientError:
        logging.exception(
            f'Message could not be sent to {queue_url}.')
        raise
    else:             
        return response 