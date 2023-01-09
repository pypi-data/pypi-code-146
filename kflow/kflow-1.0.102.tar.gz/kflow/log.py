import functools
from kflow import authn
from smart_open import open
from datetime import datetime
import logging
import pendulum

def WarehouseDatetimeLastSuccessfulJob(job_id:str,base_env:str='WarehouseProd'):
    warehouse_engine = authn.getConnectionDB(base_env)
    sql = f"""
    select last_date_loaded, datetime_started
    from job_log
    where job_name = '{job_id}' and status = 'success'
    order by datetime_started
    desc limit 1
    """
    result_proxy = warehouse_engine.execute(sql)
    for row_proxy in result_proxy:
        ## last_date_loaded is not none if it was explicitly set as a parameter.
        ## if it is not none then use that, otherwise last_date_loaded is the date the
        ## job was started.
        if row_proxy.items()[0][1] == None:
            return row_proxy.items()[1][1]
        else:
            return row_proxy.items()[0][1]

def WarehouseJobLog(row:dict, table="job_log", schema="public",base_env:str='WarehouseProd'):
    """
    Esconder autenticación
    """
    warehouse_engine = authn.getConnectionDB(base_env)
    row = {k: v for k, v in row.items() if v}
    columns = "("+','.join(list(row.keys()))+")"
    values = "("+','.join(["'"+str(a)+"'" for a in list(row.values())])+")"
    sql = f"""
        insert into "{schema}"."{table}" {columns}
        values {values}
        """
    warehouse_engine.execute(sql)

def log_python_operator(func):
    @functools.wraps(func)
    def wrapper_decorator(*args, **kwargs):

        # Before
        run_date = datetime.today()
        context = kwargs["context"]
        if "dag" in context.keys():
            WarehouseJobLog(
                {"job_name":context["dag"].dag_id,
                "job_type":"snapshot",
                "table_name":"prisma_table",
                "datetime_started":run_date,
                "datetime_finished":None,
                "last_date_loaded":context["dag_run"].conf.get('last_date'),
                "status":"started",
                "status_message":""
                })
        
        # Func
        value = func(*args, **kwargs)
        
        # After
        if "dag" in context.keys():
            WarehouseJobLog(
                {"job_name":context["dag"].dag_id,
                "job_type":"snapshot",
                "table_name":"prisma_table",
                "datetime_started":run_date,
                "datetime_finished":datetime.now(),
                "last_date_loaded":None,
                "status":"success",
                "status_message":""
                })

        return value
        
    return wrapper_decorator

def LogReporting(ti,type_log:str,details_log:list=None):

    """
    Get info from process and package it for send it to context dag how a xcom
    - - - - - - - - - 
    ti
        task instance
    type:str
        "simple": not necessary send "details_log", will save basic info (dag, tablename, date_execution, status, date_log
        "total": you must send one value in "details_log", will save  basic info + total rows
        "full": you must send four values in "details_log", will save  basic info + insert, update, delete and total rows
    details_log:list
        if type = total, you must send a list with one value, total row ingestion, e.g [100]
        if type = full, you must send a list with four values, (inserted, updated, deleted, total) it's very importan keep this order. e.g [4,2,0,100]
    """

    if ti.duration != None:
        duration = round(float(ti.duration),2)
    elif ti.duration == None:
        duration = 0

    ti.xcom_push(key='dag_duration', value=duration)
    ti.xcom_push(key='type_log', value=type_log)     

    if  type_log =='full':

        ingestion = {"ingestion":{"insert":details_log[0],
                                  "update":details_log[1],
                                  "delete":details_log[2],
                                  "total":details_log[3]}}
        ti.xcom_push(key='ingestion_detail', value=ingestion)

    elif type_log=='total':

        ingestion = {"ingestion":{"total":details_log[0]}}
        ti.xcom_push(key='ingestion_detail', value=ingestion)

    elif type_log not in ['full','total','basic']:
        logging.exception('Not recognized type_log')
        raise

    logging.info(f"Packaged Log")
                
def Failure_Dag(**context):

    """
    Get info from context for will save in log warehouse, when task finished failed
    - - - - - - - - 
    This funcion don't wait parameter, but it's neccesary:

    **context variable must contain
        key="table":value= name table procced
        key="task_id":value= task_id that procced table

    """   

    dag=context.get('task_instance').dag_id
    exec_date=context.get('execution_date').strftime('%Y%m%d')              
    end_date=pendulum.now("UTC").strftime('%Y%m%d-%H%M%S') 
    table = context["table"]
    state='failed'

    warehouse_engine = authn.getConnectionDB(base_env='WarehouseProd')
                  
    sql = f"""
        insert into staging.log_dag_execution (dag, tablename, date_execution, status, date_log)
        values ('{dag}','{table}','{exec_date}','{state}','{end_date}')
        """
    warehouse_engine.execute(sql)

    logging.info("Log saved")
   
def Success_Dag(ti,**context):

    """
    Get info from context for will save in log warehouse, when task finished failed
    - - - - - - - - 
    This funcion don't wait parameter, but it's neccesary:

    **context variable must contain
        key="table":value= name table procced
        key="task_id":value= task_id that procced table (no apply if log is basic)

    xcom must contain
        key='type_log', value with type log that you want save
        key='dag_duration', duration process
        key='ingestion_detail', dict with extra info for log         
    """   
    
    state='success'
    dag=context.get('task_instance').dag_id
    end_date=pendulum.now("UTC").strftime('%Y%m%d-%H%M%S')   
    exec_date=context.get('execution_date').strftime('%Y%m%d')

    task_id = context["task_id"]
    table = context["table"]
          
    type_log = ti.xcom_pull(key='type_log',task_ids=task_id)
    duration = ti.xcom_pull(key='dag_duration',task_ids=task_id)

    logging.info(f"type_log {type_log} - duration {duration}")    

    if type_log is None:
        type_log = 'basic'
    
    if duration is None:         
        duration = 0
   
    if type_log == 'basic':

        logging.info(f"Registring {type_log} log")
            
        sql = f"""
                insert into staging.log_dag_execution (dag, tablename, date_execution, status, date_log)
                values ('{dag}','{table}','{exec_date}','{state}','{end_date}')
                """
        
    elif type_log in ['total','full']:

        logging.info(f"Registring {type_log} log")

        log_details = ti.xcom_pull(key='ingestion_detail',task_ids=task_id)  

        sql = f"""
                insert into staging.log_dag_execution (dag, tablename, date_execution, duration, status, date_log, details)
                values ('{dag}','{table}','{exec_date}','{duration}','{state}','{end_date}',JSON_PARSE('{log_details}'))
                """.replace("'ingestion'",'"ingestion"').replace("'insert'",'"insert"').replace("'update'",'"update"').replace("'delete'",'"delete"').replace("'total'",'"total"') 
    else:
        logging.exception('Not recognized type_log')
        raise

    warehouse_engine = authn.getConnectionDB(base_env='WarehouseProd')
    warehouse_engine.execute(sql)

    logging.info("Log saved")