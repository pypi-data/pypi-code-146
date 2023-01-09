
import logging
import pendulum
import pandas as pd
from kflow import extract,load,authn
from botocore.exceptions import ClientError

def FindDuplicateforSimilarity(df1:pd.DataFrame,df2:pd.DataFrame,df1_id:str,df1_field:str,df2_field:str,ratio:float=0.90) -> dict:

    """Find Duplicate values between two DataFrame by similarity ratio

    Parameters
    ----------
    df1:pd.DataFrame
        Origin DataFrame to compare
    df2:pd.DataFrame
        Destine DataFrame to compare      
    df1_id: str
        DataFrames' Field to identify posible duplicate row in the firts df.
    df1_field: str
        Firts DataFrames' Field thant you want compare
    df2_field:
        Second DataFrames' Field thant you want compare
    ratio:float
        Tolerance percentage for similarity
    Returns
    -------
    dict
    Keys will be {df1_id}, the firts value {df1_field} and the second field the duplicate value in {df2}.
    e.g.
    {'15489':["Motor Company S.a","Motor Company SA"]} 

    Note: If dicct it's empty so there aren't duplicate values
    """

    import re    
    import difflib

    list1 = [{row[df1_id]:row[df1_field].upper()} for index, row in df1.iterrows()]
    list2 = [row[df2_field].upper() for index, row in df2.iterrows()]

    duplicate = {}
    
    for value in list1:
        value_string = list(value.values())[0]
        match = difflib.get_close_matches(value_string,list2,cutoff=ratio)
        if len(match) > 0:      
            duplicate[list(value.keys())[0]] = [match[0],value_string]
        else:
            continue   
    
    return duplicate

def ExtractSubString(list_values:list,function:str,pattern:str=None) -> pd.DataFrame:

    """Find Duplicate values between two DataFrame by similarity ratio

    Parameters
    ----------
    list_values:list
        List of value that you want extract substring
    function:str
        You can use some default possible: 
                  "fiscal_suffix": S.A, LTDA ect
                  "web_domains": .com, .cl, .org ect
                  "suffix_domains": Fiscal Suffix or Web Domains
    pattern:str=None
        You can get substring with custom regex parttern, default is None.
    Returns
    -------
    pd.DataFrame
    DataFrame with two columns, substring finded and a example in dataset.
    """
    import re
    import pandas as pd

    if function == "fiscal_suffix":
        pattern = "(\ ?)(\.?)([LIMITADASPC]+)(\ ?)(\.?)([LIMITADASPC]?)(\.?)( ?)$"  # Fiscal Suffix (S.A, LTDA ect)
    if function == "web_domains":
        pattern = "(\.)[A-Z]{2,5}(\.[A-Z]{2,5})?"  # Web Domains (.com, .cl, .org ect)  

    if function == "suffix_domains":
        pattern = "(\ ?)(\.?)([LIMITADASPC]+)(\ ?)(\.?)([LIMITADASPC]?)(\.?)( ?)$|(\.)[A-Z]{2,5}(\.[A-Z]{2,5})?" # Fiscal Suffix or Web Domains
    else:
        pattern = pattern

    SubString = {}

    for value in list_values:
        X = re.search(pattern,value)  

        if type(X) == re.Match:        
                SubString[str(X.group())] = value
        else:   
            continue

    df = pd.DataFrame(SubString.items(), columns=['substring','example'])
    
    return df

def DeleteCompaniesHubspot(delete_companies:list,hubspot_env:str,):

    """Delete Companies on Hubspot 

    Parameters
    ----------
    delete_companies:list
        List must contain id_hubspot that companies you want delete   
    hubspot_env:str        
        HubspotProd - ambiente productivo
        HubspotTest - ambiente de pruebas
     
    """
    from kflow import authn  
    from hubspot.crm.companies import BatchInputSimplePublicObjectId, ApiException

    client = authn.getHubspotClient(hubspot_env)  
        
    delete_list = [{"id":str(x)} for x in delete_companies]        
    batch_input_simple_public_object_id = BatchInputSimplePublicObjectId(inputs=delete_list)

    try:
        api_response = client.crm.companies.batch_api.archive(batch_input_simple_public_object_id=batch_input_simple_public_object_id)                
    except ApiException:
        raise

def delete_queue_message(queue_url, receipt_handle):
    """
    Deletes the specified message from the specified queue.
    """
    sqs_client = authn.awsClient(service='sqs')

    try:
        response = sqs_client.delete_message(QueueUrl=queue_url,
                                             ReceiptHandle=receipt_handle)
    except ClientError:
        logging.exception(
            f'Could not delete the meessage from the - {queue_url}.')
        raise
    else:        
        return response

def Slack_Task_Notification_Fail(context):

    """
    Send messege notification to Slack group when your dag execute FAILED
    
    Nota: esta función solo recibe parametros de contexto del DAG, estudiar la posibilidad que reciba parametros personalizado como el grupo al cual
    enviar el mensaje y que tipo de mensaje enviar así contener en una sola función ambos casos (fail/success)

    """

    SLACK_CONN_ID = 'slack_team'      

    from airflow.hooks.base_hook import BaseHook
    from airflow.contrib.operators.slack_webhook_operator import SlackWebhookOperator

    slack_webhook_token = BaseHook.get_connection(SLACK_CONN_ID).password

    slack_msg = """
        :red_circle: Task Failed, I'm sorry... :sweat:
        *Task*: {task}  
        *Dag*: {dag} 
        *Execution Time*: {exec_date}  
        *Log Url*: {log_url}            
        """.format(
        task=context.get('task_instance').task_id,
        dag=context.get('task_instance').dag_id,
        ti=context.get('task_instance'),
        exec_date=context.get('execution_date'),
        log_url=context.get('task_instance').log_url)

    failed_alert = SlackWebhookOperator(
        task_id='slack_notification',
        http_conn_id=SLACK_CONN_ID,
        webhook_token=slack_webhook_token,
        message=slack_msg,
        username='airflow')

    return failed_alert.execute(context=context)

def Slack_Task_Notification_Success(context):

    """
    Send messege notification to Slack group when your dag execute SUCCESS
    
    Nota: esta función solo recibe parametros de contexto del DAG, estudiar la posibilidad que reciba parametros personalizado como el grupo al cual
    enviar el mensaje y que tipo de mensaje enviar así contener en una sola función ambos casos (fail/success)

    """

    SLACK_CONN_ID = 'slack_team'        

    from airflow.hooks.base_hook import BaseHook
    from airflow.contrib.operators.slack_webhook_operator import SlackWebhookOperator

    slack_webhook_token = BaseHook.get_connection(SLACK_CONN_ID).password

    slack_msg = """
        :large_green_circle: Task Success, Good Job!! :muscle: 
        *Task*: {task}  
        *Dag*: {dag} 
        *Execution Time*: {exec_date}                           
        """.format(
        task=context.get('task_instance').task_id,
        dag=context.get('task_instance').dag_id,
        ti=context.get('task_instance'),
        exec_date=context.get('execution_date'))

    success_alert = SlackWebhookOperator(
        task_id='slack_notification',
        http_conn_id=SLACK_CONN_ID,
        webhook_token=slack_webhook_token,
        message=slack_msg,
        username='airflow')

    return success_alert.execute(context=context)  

def create_vecna_subscription(payload,headers=None):
    
    """ Calls API that creates subscriptions for testing Vecna """

    import http.client
    import json
    import logging

    conn = http.client.HTTPSConnection("53e9ntbka2.execute-api.us-east-1.amazonaws.com")
    payload = json.dumps(payload)

    if headers == None:
        headers = {
        'Authorization': 'Token Y2w4NHVhNzU5MDAwMTA5bDNnYTVjOXl1dDpETVNLQURLTUxTUUE=',
        'Content-Type': 'application/json'
        }
    else:
        headers=headers

    conn.request("POST", "/subscriptions", payload, headers)
    res = conn.getresponse()
    data = res.read()
    
    return data.decode("utf-8")


def read_hubspot_properties(object:str,hubspot_env:str="HubspotProd"):

    import hubspot
    from pprint import pprint
    from hubspot.crm.properties import ApiException

    client = client = authn.getHubspotClient(hubspot_env)

    try:
        api_response = client.crm.properties.core_api.get_all(object_type=object, archived=False)
        
    except ApiException as e:
        print("Exception when calling core_api->get_all: %s\n" % e)

    dict_response = api_response.to_dict()['results']
    list_properties = {property['name']:property['label'] for property in dict_response}
    
    return list_properties