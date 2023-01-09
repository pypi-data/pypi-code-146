import os
import logging
from kflow import extract

def _getRuntimeEnviroment() -> str:

    import os

    s3 = os.environ.get("S3")

    env = 'dev'

    if s3 == None:
        try:
            from airflow.models import Variable        
            try:
                env = Variable.get("ENV")
            except KeyError:
                logging.warning("Variable ENV not found, we default to local environment")
        except ModuleNotFoundError as err:
            logging.warning("Airflow not found, we default to local environment")        
            env = 'dev'
    else:
        env = 'dev'

    return env

def awsClient(type_auth:str='client',service:str='s3'):  # Old S3Connect

    """
    Get S3 client
    
    service:str    
        s3: to get acceses Data Lake
        sqs: to get acceses sqs service

    Return
    ----------------
    S3 client
    """

    import boto3 

    env = _getRuntimeEnviroment()

    if env == 'prod':
        from airflow.models import Variable
        try:
            aws_access_key_id = Variable.get("aws_access_key_id")
            aws_secret_access_key = Variable.get("aws_secret_access_key")
        except KeyError:
            logging.warning("Variable ENV not found, we default to local environment")
    elif env == 'dev':
        S3_conn = os.environ["S3"].strip('][').split(',')
        aws_access_key_id = S3_conn[0]
        aws_secret_access_key = S3_conn[1]
    else:
        raise ValueError('Current environment not recognized')

    if type_auth == 'client':

        s3_auth = boto3.client(service,
                                aws_access_key_id=aws_access_key_id,
                                aws_secret_access_key=aws_secret_access_key,
                                region_name='us-east-1')
    elif type_auth == 'session':

        s3_auth = boto3.Session( aws_access_key_id=aws_access_key_id,
                                aws_secret_access_key=aws_secret_access_key)

    return s3_auth

def getHubspotClient(hubspot_env:str):

    """
    Get client to connect Hubspot

    Parameters
    --------------------
    hubspot_env:str        
        HubspotProd - ambiente productivo
        HubspotTest - ambiente de pruebas
    
    Return
    --------------------
    Hubspot client
    """

    import hubspot

    env = _getRuntimeEnviroment()

    if env == 'prod':
        from airflow.models import Variable
        try:
            conn_hub = Variable.get(f"{hubspot_env}")
        except KeyError:
            logging.warning(f"Variable {hubspot_env} not found, we default to local environment")
    elif env == 'dev':
        try:
            conn = extract.LakeFileAsJson("auth/","authn_klog.json")
            conn_hub = conn[hubspot_env]
        except KeyError:
            logging.error(f"Variable {hubspot_env} not found in environment, cannot stablish connection")
            return
    else:
        raise ValueError('Current environment not recognized')
    
    client = hubspot.Client.create(access_token=conn_hub)
    
    return client

def getConnectionDB(base_env:str):
    
    """
    Get database connection
    Parameters
    ----------
    base_env:str
        "WarehouseProd" - ambiente productivo del warehouse en Redshift
        "PrismaProd" - ambiente productivo de prisma en RDS
    Return
    ---------- 
        Database connection
    """
    from sqlalchemy import create_engine

    env = _getRuntimeEnviroment()    

    if env == "prod":
        try:      
            from airflow.providers.postgres.hooks.postgres import PostgresHook            
            hook = PostgresHook(postgres_conn_id=base_env)  # WarehouseProd / PrismaProd
            connection = hook.get_connection(base_env)
            
            if base_env == 'WarehouseProd':                         
                conn_bd = f"redshift+psycopg2://{connection.login}:{connection.password}@{connection.host}:{connection.port}/{connection.schema}"
            elif base_env == 'PrismaProd':
                conn_bd = f"postgresql://{connection.login}:{connection.password}@{connection.host}:{connection.port}/{connection.schema}"
            else:
                raise ValueError('Current BD environment not recognized')
        except:
            logging.warning(f"base_env {base_env} not found")
            raise    
    elif env == 'dev':
        try:
            conn = extract.LakeFileAsJson("auth/","authn_klog.json")
            conn_bd = conn[base_env]   # WarehouseProd / PrismaProd
        except KeyError:
            logging.error(f"Variable {base_env} not found in environment, cannot stablish connection")
            raise
    else:
        raise ValueError('Current environment not recognized')
    
    bd_engine = create_engine(conn_bd)
    
    return bd_engine

def getConnectionGoogleSheet(auth:str="SERVICE"):    # old GoogleSheetAuth
    
    """
    Devuelve el servicio de Google Sheets
    
    Parameters
    ----------
    auth: str
        Indica tipo de autenticación a usar. Tipos:
        * SERVICE: Autenticación por cuenta de servicio. Esta se basa en una service
        account a la que hay que compartirle el sheet que queramos accesar.
    """
   
    from googleapiclient.discovery import build
    from google.oauth2 import service_account

    scopes = ['https://www.googleapis.com/auth/spreadsheets']
    if auth == "SERVICE":
        service_account_json = extract.LakeFileAsJson("auth/","data-and-bi-342313-9363b0ec39cf.json")
        credentials = service_account.Credentials.from_service_account_info(service_account_json, scopes=scopes)
        return build('sheets', 'v4', credentials=credentials)
    else:
        logging.error("Unidentified auth")
        return None

def getGithubToken(repo:str="teu-ai/etl"):

    """
    DOCUMENTAR
    """

    from github import Github

    env = _getRuntimeEnviroment()

    if env == 'prod':
        from airflow.models import Variable
        try:
            conn_github = Variable.get("token_github")
        except KeyError:
            logging.warning(f"Variable 'token_github' not found, we default to local environment")
    elif env == 'dev':
        try:
            conn = extract.LakeFileAsJson("auth/","authn_klog.json")
            conn_github = conn["token_github"]
        except KeyError:
            logging.error(f"Variable 'token_github' not found in environment, cannot stablish connection")
            return
    else:
        raise ValueError('Current environment not recognized')
       
    g = Github(conn_github)
    repo_cliente = g.get_repo(repo)
    
    return repo_cliente

def getIAMRole(role:str):
    """
    DOCUMENTAR
    """

    env = _getRuntimeEnviroment()

    if env == 'prod':
        from airflow.models import Variable
        try:
            iam_role = Variable.get(role)
        except KeyError:
            logging.warning(f"Variable {role} not found, we default to local environment")
    elif env == 'dev':
        try:
            conn = extract.LakeFileAsJson("auth/","authn_klog.json")
            iam_role = conn[role]
        except KeyError:
            logging.error(f"Variable {role} not found in environment, cannot stablish connection")
            return
    else:
        raise ValueError('Current environment not recognized')
    
    return iam_role
