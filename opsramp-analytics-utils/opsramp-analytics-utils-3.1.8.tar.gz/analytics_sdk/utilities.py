import os
import time
import datetime
import logging
from io import BytesIO
from datetime import datetime
import json
import traceback

from urllib.request import urlopen
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from flask.wrappers import Response

import jwt
import boto3
import botocore
from botocore.exceptions import NoCredentialsError
import flask
import requests

from .constants import DATETIME_FORMAT
logger = logging.getLogger(__name__)

BASE_API_URL = os.getenv('DATA_API_BASE_URL', '')
API_RETRY = int(os.getenv('API_RETRY', 3))
API_KEY = os.getenv('API_KEY')
API_SECRET = os.getenv('API_SECRET')
BASE_API_URL = os.getenv('DATA_API_BASE_URL', '')
PLATFORM_ROUTE = os.getenv("PLATFORM_ROUTE")
APP_ID = os.getenv('APP_ID')
API_TIME_STACKS = int(os.getenv('API_TIME_STACKS', 5))
APP_DISPLAY_NAME = os.getenv('APP_DISPLAY_NAME', APP_ID)

from .renderer.excel import ExcelRenderer
from .renderer.pdf import PDF

storage_name = os.getenv('STORAGE_NAME')

global ACCESS_KEY_ID, SECRET_ACCESS_KEY, REGION_NAME, BUCKET_NAME, ACCESS_HEADER, TOKEN_RETRIES

if storage_name == 's3':
    ACCESS_KEY_ID = os.getenv('ACCESS_KEY_ID')
    SECRET_ACCESS_KEY = os.getenv('SECRET_ACCESS_KEY')
    REGION_NAME = os.getenv('REGION_NAME')
    BUCKET_NAME = os.getenv('BUCKET_NAME')
elif storage_name == 'ceph':
    ACCESS_KEY_ID = os.getenv('ACCESS_KEY_ID')
    SECRET_ACCESS_KEY = os.getenv('SECRET_ACCESS_KEY')
    BUCKET_NAME = os.getenv('BUCKET_NAME', 'analytics-apps')
    ENDPOINT_URL = os.getenv('ENDPOINT_URL')
else:
    logger.info("No storages are found")
TOKEN_RETRIES = 0
ACCESS_HEADER = None

def get_token():
    headers = {"Content-Type" : "application/x-www-form-urlencoded" , "Accept" : "application/json"};
    post_data = {"grant_type": "client_credentials", "client_id" : API_KEY, "client_secret" : API_SECRET};
    token_url = BASE_API_URL + "/auth/oauth/token";
    response = requests.post(token_url,data=post_data,headers=headers,verify=False);
    json = response.json();
    auth = str(json["access_token"])
    return auth


def get_jwt_token():
    try:
        jwt_token = flask.request.cookies.get('OPSRAMP_JWT_TOKEN', '')
    except:  # outside Flask
        jwt_token = os.getenv('OPSRAMP_JWT_TOKEN', '')

    return jwt_token


def get_headers():
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'Authorization': f'Bearer {get_token()}'
    }

    return headers


def login_get_headers():
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'Authorization': f'Bearer {get_jwt_token()}'
    }

    return headers


def get_auth_token():
    logging.info('invoking auth token call...')
    headers = {"Content-Type" : "application/x-www-form-urlencoded" , "Accept" : "application/json"}
    post_data = {"grant_type": "client_credentials", "client_id" : API_KEY, "client_secret" : API_SECRET}
    token_url = BASE_API_URL + "/auth/oauth/token"
    response = requests.post(token_url,data=post_data,headers=headers,verify=False)
    json = response.json()
    auth = str(json["token_type"]) + " " + str(json["access_token"])
    global ACCESS_HEADER
    ACCESS_HEADER = {"Content-Type" : "application/json" ,"Accept" : "application/json" , "Authorization" : auth }


def call_requests(method, url, params=None, data=None, json=None, verify=True):
    retry = 1
    resp = None
    if ACCESS_HEADER is None:
        get_auth_token()
        global TOKEN_RETRIES
        TOKEN_RETRIES = 0
    while retry <= API_RETRY:
        try:
            resp = requests.request(method, url, params=params, data=data, json=json, headers=ACCESS_HEADER, verify=verify)
            if resp.status_code == 407:
                if TOKEN_RETRIES < 5:
                    logging.info(f'Token expired, re-generating token..{TOKEN_RETRIES}' )
                    TOKEN_RETRIES +=1
                    time.sleep(TOKEN_RETRIES * 2)
                    get_auth_token()
                    call_requests(method, url, params=params, data=data, json=json, verify=verify)
                else:
                    TOKEN_RETRIES = 0
                    raise Exception(f'API Fetching failed {url}')
            if not resp.ok:
                time.sleep(retry * 2)
                retry+=1
                continue
        except requests.exceptions.ConnectionError:
            time.sleep(retry * 2)
            retry+=1
            continue
        
        TOKEN_RETRIES = 0
        return resp
    
    return resp


def login_call_requests(method, url, params=None, data=None, json=None, verify=True):
    headers = login_get_headers()
    retry = 1
    resp = None
    while retry <= API_RETRY:
        try:
            resp = requests.request(method, url, params=params, data=data, json=json, headers=headers, verify=verify)
            if not resp.ok:
                time.sleep(retry * 2)
                retry+=1
                continue
        except requests.exceptions.ConnectionError:
            time.sleep(retry * 2)
            retry+=1
            continue

        return resp

    return resp


def call_get_requests(url, params=None, verify=True):
    return call_requests('GET', url, params, verify=verify)


def call_post_requests(url, params=None, data=None, verify=True):
    return call_requests('POST', url, params, data, verify=verify)


def call_put_requests(url, params=None, data=None, verify=True):
    return call_requests('PUT', url, params, data, verify=verify)


def login_call_get_requests(url, params=None, verify=True):
    return login_call_requests('GET', url, params, verify=verify)


def is_authenticated():
    REQUIRE_AUTH_REDIRECT = os.getenv('REQUIRE_AUTH_REDIRECT') == 'true'
    if not REQUIRE_AUTH_REDIRECT:
        return True

    url = f'{BASE_API_URL}/api/v2/users/me'
    res = login_call_get_requests(url)
    return res.status_code == 200


def login_required(view):
    '''Decorator that check authentication'''
  
    def wrap(*args, **kwargs):
        if not is_authenticated():
            return Response('Not authorized', status=401)
        result = view(*args, **kwargs)
        return result
    return wrap


def get_epoc_from_datetime_string(str_datetime):
    timestamp = datetime.strptime(str_datetime, DATETIME_FORMAT).timestamp()
    return timestamp


def get_result_by_run(run_id, field=None, default_value=None):
    try:
        # run_id= f'{PLATFORM_ROUTE}/{run_id}/json/{run_id}'
        if storage_name == 's3':
            run_id= f'{PLATFORM_ROUTE}/{run_id}/json/{run_id}'
            s3 = get_s3_client()
            res_object = s3.get_object(Bucket=BUCKET_NAME,Key=run_id)
            serializedObject = res_object['Body'].read()
            result = json.loads(serializedObject)
            if field:
                result = result.get(field, default_value)
            return result
        elif storage_name == 'ceph':
            run_id= f'{APP_ID.lower()}/{run_id}/json/{run_id}'
            s3 = get_ceph_resource()
            data = BytesIO()
            res_object = s3.Bucket(BUCKET_NAME).download_fileobj(Fileobj=data,Key=run_id)   
            res_object = data.getvalue()
            result = json.loads(res_object)
            if field:
                result = result.get(field, default_value)
            return result
        else:
            logger.info("No storages are found")
    except Exception:
        logger.error('An error occurred (NoSuchKey) when calling the GetObject operation: The specified key does not exist')
        pass


def get_response(url, type, params=None):
    start_time = int(time.time())
    logging.info(f'api type: {type}, : url : {url}')
    res = call_get_requests(url, params=None, verify=True)
    duration = int(time.time()) - start_time
    if duration > API_TIME_STACKS:
        logging.info(f'Get {type} API response took %d (greater than %d) seconds, url : {url}', duration, API_TIME_STACKS)
    return res


def get_ses_client():
    return boto3.client('ses',
                        region_name=REGION_NAME,
                        aws_access_key_id=ACCESS_KEY_ID,
                        aws_secret_access_key=SECRET_ACCESS_KEY)


def get_s3_client():
    return boto3.client('s3',
                        region_name=REGION_NAME,
                        aws_access_key_id=ACCESS_KEY_ID,
                        aws_secret_access_key=SECRET_ACCESS_KEY)
    

def get_ceph_resource():
    return boto3.resource('s3',
                            endpoint_url=ENDPOINT_URL,
                            aws_access_key_id=ACCESS_KEY_ID,
                            aws_secret_access_key=SECRET_ACCESS_KEY)


def get_ceph_client():
    return boto3.client('s3',
                          endpoint_url=ENDPOINT_URL,
                          aws_access_key_id=ACCESS_KEY_ID,
                          aws_secret_access_key=SECRET_ACCESS_KEY)



def send_email(subject, from_email, to_emails, body, attachment=None):
    message = MIMEMultipart()
    message['Subject'] = subject
    message['From'] = from_email
    message['To'] = to_emails

    # message body
    part = MIMEText(body, 'html')
    message.attach(part)

    if attachment:
        attachment_body = urlopen(attachment).read()
        part = MIMEApplication(attachment_body)
        part.add_header('Content-Disposition', 'attachment', filename=attachment)
        message.attach(part)

    resp = get_ses_client().send_raw_email(
        Source=message['From'],
        Destinations=to_emails.split(','),
        RawMessage={
            'Data': message.as_string()
        }
    )

    return resp


def upload_to_storage(content, location):
    '''
    :param: content: bytes
    :param: location: str
    '''
    if storage_name == 's3':
        s3 = boto3.resource('s3',
                            region_name=REGION_NAME,
                            aws_access_key_id=ACCESS_KEY_ID,
                            aws_secret_access_key=SECRET_ACCESS_KEY)
        object_url = f'https://{BUCKET_NAME}.s3.{REGION_NAME}.amazonaws.com/{location}'
        try:
            s3.Bucket(BUCKET_NAME).put_object(Body=content,
                                                 Key=location)
            #return object_url
            return location
        except Exception:
            pass
    elif storage_name == 'ceph':
        try:
            s3 = get_ceph_resource()
            bucket_check = s3.Bucket(BUCKET_NAME) in s3.buckets.all()
            
            if bucket_check:
                logger.info(f'{BUCKET_NAME} Bucket already exists!')
            else:
                logger.info(f'{BUCKET_NAME} Bucket does not exist!')
                try:
                    bucket = s3.Bucket(BUCKET_NAME)
                    bucket.create()
                except botocore.parsers.ResponseParserError as error:
                #Bucket is created is successfully, but throwing an error. So that we are catching and passing that error(But not throwing that error)
                    bucket_check = s3.Bucket(BUCKET_NAME) in s3.buckets.all()
                    if bucket_check:
                        logger.info(f'{BUCKET_NAME} bucket created...')
                    else:
                        logger.info(f'{BUCKET_NAME} bucket is not created...')
                    pass
            
            s3.Bucket(BUCKET_NAME).put_object(Bucket=BUCKET_NAME,
                                            Key=location,
                                            Body=content)
            #return object_url
            return location
        except Exception:
            pass
    else:
        logger.info("No storages are found")


def generate_pdf(analysis_run):
    logger.info(f'{analysis_run} :: Entered into pdf generation process')
    try:
        url = os.getenv("PDF_SERVICE")
        current_date = datetime.now()
        # file_name = APP_ID.lower() + '-' + pdf.analysis_run[:8] + '-' + current_date.strftime("%Y-%m-%d-%H-%M-%S") + '.pdf'
        report_path = ''
        if storage_name == 's3':
            report_path = PLATFORM_ROUTE
        elif storage_name == 'ceph':
            report_path = APP_ID.lower()
        pdf = PDF(analysis_run, url, report_path, current_date.strftime("%Y-%m-%d-%H-%M-%S"))
        file_name = pdf.prepare_file_name(APP_ID.lower(), 'pdf')
        file_path = pdf.report_path + '/' + pdf.analysis_run + '/pdf/' + file_name
        data = {
            'domain': BASE_API_URL,
            'report': PLATFORM_ROUTE,
            'run': pdf.analysis_run,
            'route': '/full-view',
            'token': get_token(),
            'app_id': APP_ID,
            'size': 'A4',
            'storage': storage_name,
            'file_name': file_name,
            'file_path': file_path
        }
        
        gen_retry = 1
        while gen_retry <= 2:
            logging.info(f'{pdf.analysis_run} :: pdf generation trying {gen_retry} time..')
            gen_retry += 1
            logging.info(f'b4 generation >> full file path : {file_path}')
            response = pdf.generate(data)
            logging.info(f'after generation >> full file path : {file_path}')
            if response == 504:
                storage_retry = 1
                file_found = False
                while storage_retry <= API_RETRY:
                    logging.info(f'{pdf.analysis_run} checking the file is existing in storage or not {storage_retry} time..')
                    file_found = is_file_in_storage(file_path)
                    if file_found == True:
                        logging.info(f'{pdf.analysis_run} the pdf file is found in storage')
                        return file_path
                    else:
                        time.sleep(storage_retry * 30)
                        storage_retry += 1
                        logging.info(f'{pdf.analysis_run} pdf not found in storage trying for {storage_retry} time..')
                        continue
            else:
                return response
        raise Exception(f'Generate_pdf:: pdf generation failed after max tries ({API_RETRY}), for run ::: {pdf.analysis_run}')
    except Exception as e:
        traceback.print_exc()
        err_msg = f'Generate_pdf:: Exeception - pdf generation failed after max tries({API_RETRY}), for run ::: {analysis_run}'
        raise Exception(err_msg)


def is_file_in_storage(file_path: str):
    try:
        if storage_name == 's3':
            s3 = get_s3_client()
            res_object = s3.get_object(Bucket=BUCKET_NAME,Key=file_path)
            return True
        elif storage_name == 'ceph':
            s3 = get_ceph_resource()
            data = BytesIO()
            res_object = s3.Bucket(BUCKET_NAME).download_fileobj(Fileobj=data,Key=file_path)
            return True
        else:
            return False
    except Exception as e:
        return False


def generate_excel(analysis_run, orgId, client_name, excel_data, report_gen_start_time, report_gen_completed_time, file_name=None):
    try:
        excel_renderer = ExcelRenderer(analysis_run, orgId, client_name, excel_data, report_gen_start_time, report_gen_completed_time)
        workbook = excel_renderer.render()
    except Exception as ex:
        raise ex

    if file_name:
        output = None
        workbook.save(file_name)
    else:
        output = BytesIO()
        workbook.save(output)

    return output


def diff_sec(st, et):
    difference = int(et - st)
    return difference


def update_status_url(analysisRunId, tenantId, genStime, genEtime, status=None):

    url = BASE_API_URL + f'/reporting/api/v3/tenants/{tenantId}/runs/{analysisRunId}'
    data={
            "status" : status,
            "runDurStartDate" : genStime,
            "runDurEndDate" : genEtime
        }
    
    api_proce_before_time = time.time()
    res = call_put_requests(url , data=json.dumps(data), verify=False);
    api_proce_after_time = time.time()
    api_proce_diff = diff_sec(api_proce_before_time, api_proce_after_time)
    if api_proce_diff > API_TIME_STACKS:
        logging.info('Status update response took %d (greater than %d) seconds', api_proce_diff, API_TIME_STACKS)
    logger.info('Status update response is %s', res)


def update_results_url(gen_start_time, analysisRunId, tenantId, json_result_url=None, gen_completed_time=None, excel_result_url=None, pdf_result_url=None, failure_reason=None, status=None):

    url = BASE_API_URL + f'/reporting/api/v3/tenants/{tenantId}/runs/{analysisRunId}'
    
    if storage_name == 'ceph':
        if excel_result_url is not None:
            excel_result_url = f'{BUCKET_NAME}/{excel_result_url}'
        if pdf_result_url is not None:
            pdf_result_url = f'{BUCKET_NAME}/{pdf_result_url}'
            
    data={
            "status" : status,
            "resultUrl" : json_result_url,
            "pdfFilePath" : pdf_result_url,
            "xlsxFilePath" : excel_result_url,
            "repGenStartTime" : gen_start_time,
            "repGenEndTime" : gen_completed_time,
            "failureReason" : failure_reason
        }

    api_proce_before_time = time.time()
    res = call_put_requests(url , data=json.dumps(data), verify=False);
    api_proce_after_time = time.time()
    api_proce_diff = diff_sec(api_proce_before_time, api_proce_after_time)
    if api_proce_diff > API_TIME_STACKS:
        logging.info('Database update response took %d (greater than %d) seconds', api_proce_diff, API_TIME_STACKS)
    logger.info('Database update response is %s', res)


#Upload excel file to s3
def upload_excel_s3(local_file, bucket, s3_file):
    retry = 1
    s3 = get_s3_client()
    while retry <= API_RETRY:
        try:
            s3.upload_file(local_file, bucket, s3_file)
            url = f'https://{bucket}.s3.{REGION_NAME}.amazonaws.com/{s3_file}'
            logger.info('Upload successful, result url is %s', url)
        
            delete_excel_file(local_file)
            return s3_file
        except FileNotFoundError:
            logger.info('File was not found')
            return False
        except NoCredentialsError:
            logger.info('Invalid credentials')
            return False
        except Exception as e:
            time.sleep(retry * 2)
            retry+=1
            if retry > API_RETRY:
                raise e
            continue


#Upload excel file to ceph
def upload_excel_ceph(local_file, bucket, s3_file):
    retry = 1
    s3 = get_ceph_resource()
    while retry <= API_RETRY:
        try:
            s3.Bucket(BUCKET_NAME).upload_file(Filename = local_file, Key = s3_file)
            logger.info('Upload successful')
            delete_excel_file(local_file)
            return s3_file
        except FileNotFoundError:
            logger.info('File was not found')
            return False
        except NoCredentialsError:
            logger.info('Invalid credentials')
            return False
        except Exception as e:
            time.sleep(retry * 2)
            retry+=1
            if retry > API_RETRY:
                raise e
            continue


#Delete excel_file from local path
def delete_excel_file(source_path):
    try:
        os.remove(source_path)
        logger.info('Excel file successfully deleted')
    except OSError as e:
        logger.info(f'Failed to delete: %s : %s % {source_path, e.strerror}')


#Generate excel file
def generate_excel_file(run_id, orgId, client_name, report_gen_start_time, report_gen_completed_time):
    logger.info('Entered into excel generation process')
    excel_data=get_result_by_run(run_id, 'excel-data', {})
    reportname = f"{APP_ID.lower()}-{run_id[:8]}" + '-' + datetime.now().strftime('%Y-%m-%d-%I-%M-%S') + '.xlsx'
    filepath = './' + reportname
    generate_excel(run_id, orgId, client_name, excel_data, report_gen_start_time, report_gen_completed_time, filepath)
    # excel_file_location = f'{PLATFORM_ROUTE}/{run_id}/xls/' + reportname
    if storage_name == 's3':
        excel_file_location = f'{PLATFORM_ROUTE}/{run_id}/xls/' + reportname
        excel_url = upload_excel_s3(filepath, BUCKET_NAME, excel_file_location)
    elif storage_name == 'ceph':
        excel_file_location = f'{APP_ID.lower()}/{run_id}/xls/' + reportname
        excel_url = upload_excel_ceph(filepath, BUCKET_NAME, excel_file_location)
    else:
        logger.info("No storages are found")
    return excel_url


def init_mail(org_id, run_id):
    logger.info('Entered into init_mail method')
    try:
        # /tenants/{tenantId}/runs/{id}/sends
        url = BASE_API_URL + f'/reporting/api/v3/tenants/{org_id}/runs/{run_id}/sends'
        data = {}
        t1 = int(time.time())
        res = call_post_requests(url , data=json.dumps(data), verify=False)
        t2 = int(time.time())
        duration = t2-t1
        if duration > API_TIME_STACKS:
            logging.info('Status update response took %d (greater than %d) seconds', duration, API_TIME_STACKS)
        logger.info('Status update response is %s', res)
    except Exception as e:
        logger.error("Exception raised due to : " + repr(e))
        traceback.print_exc()
    logger.info('finished init_mail method')



def send_internal_failure_notification_mail(run_id, app_name, err_msg, partner_id, partner_name, client_id, client_name):
    logger.info('Entered into send_internal_failure_notification_mail method')
    try:
        url = BASE_API_URL + f'/reporting/api/v3/sendInternalFailureNotifications'
        data = {
            "runId": run_id,
            "appName": app_name,
            "exception": err_msg,
            "partnerId": partner_id,
            "partnerName": partner_name,
            "clientIds": client_id,
            "clientNames": client_name
        }
        t1 = int(time.time())
        res = call_post_requests(url , data=json.dumps(data), verify=False)
        t2 = int(time.time())
        duration = t2-t1
        if duration > API_TIME_STACKS:
            logging.info('Send internal failure notification mail response took %d (greater than %d) seconds', duration, API_TIME_STACKS)
        logger.info('Send internal failure notification mail response is %s', res)
    except Exception as e:
        raise e
        logger.error("Exception raised due to : " + repr(e))
        traceback.print_exc()
    logger.info('finished send_internal_failure_notification_mail method')



def upload_excel(analysis_run, excel_file):
    timestamp = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
    s3_path = f'{analysis_run.analysis.app.slug}/excel/{timestamp}.xlsx'

    return upload_to_storage(excel_file, s3_path)


"""
Method to read summary response and get the required values to showcase in the summary / overview pages of the result files
Inpute values:
    param1: run_id - actual run id of the generated run
    param2: summary_key - this is the key which is stored with summary response of a run in the metafile(json) stored in the cloud
    param3: value_by - defines the which type information is requested by end user.
        values:
            client_logo
            partner_logo
            client_name
            partner_name
            description
            last_run
"""
def get_summary_details(run_id, summary_key, value_by):
    value = ''
    if value_by is None or summary_key is None:
        return value
    if (len(value_by) == 0 or len(summary_key) == 0):
        return value
    summary_response = get_result_by_run(run_id, summary_key, {})
    if len(summary_response) <= 0:
        return value

    if value_by == 'client_logo':
        return get_tenant_logo(summary_response, 'client')
    elif value_by == 'partner_logo':
        return get_tenant_logo(summary_response, 'partner')
    elif value_by == 'last_run':
        return get_last_run(summary_response)
    elif value_by == 'description':
        return get_app_description(summary_response)
    elif value_by == 'partner_name':
        return get_tenant_name(summary_response, 'partner')
    elif value_by == 'client_name':
        return get_tenant_name(summary_response, 'client')
    else:
        return value


def get_tenant_logo(summary_res, context):
    logo = ''
    if context == 'partner':
        logo = summary_res['partner_logo_path']
    else:
        logo = summary_res['client_logo_path']
    return logo


def get_tenant_name(summary_res, context):
    name = ''
    if context == 'client':
        name = summary_res['client_name']
    else:
        name = summary_res['partner_name']
    return name


def get_last_run(summary_res):
    return summary_res['create_date']


def get_app_description(summary_res):
    return summary_res['app_description']


def get_paginated_api_results(method, url, data, type, add_pageNo=True):
    resp = []
    page_no=1
    nextPage= True
    pageSize= 100

    try:
        while (nextPage != False):
            data = json.loads(data)
            if "pageNo" in data:
                data["pageNo"] = page_no
                data["pageSize"] = pageSize
            data=json.dumps(data)
            if method == 'POST':
                res = get_post_request_results(url, data, type)
            else:
                if add_pageNo:
                    uri = url + f'&pageNo={page_no}&pageSize={pageSize}'
                else:
                    uri = url
                res = get_response(uri, type)

            if res == None or not res.ok:
                logger.error('Get %s API is failed, url %s', type, url)
                return resp
            elif "results" not in res.json() or len(res.json()['results'])==0 :
                logger.error('Get %s API results are empty, url is %s', type, url)
                return None
            else:   
                result = res.json()['results']
                resp.append(result)
        
                if "nextPage" not in res.json():
                    resp = []
                    logger.error('Get %s nextPage keyword is missing in url %s', type, url)
                    resp = [item for sublist in resp for item in sublist]
                    return resp
        
                nextPage=res.json()['nextPage']
                page_no+=1
        
        resp = [item for sublist in resp for item in sublist] # To eliminate list of list (ex: [[data:{}]] -> [data:{}])
    except Exception as e:
        traceback.print_exc()
    return resp


def get_post_request_results(url, data, type):
    start_time = int(time.time())
    logging.info(f'api type: {type}, : url : {url}')

    res = call_post_requests(url, data=data, verify=False)
    duration = int(time.time()) - start_time
    if duration > API_TIME_STACKS:
        logging.info(f'Get {type} API response took %d (greater than %d) seconds, url : {url}', duration, API_TIME_STACKS)
    return res


def get_post_opsql_count_results(url, data, type):
    res = get_post_request_results(url, data, type)
    if res == None or not res.ok:
        logger.error('FAILED :' + type)
        return None
    elif "count" not in res.json() or len(res.json()) == 0:
        logger.error('Result are Empty for ' + type)
        return None
    else:
        resp = res.json()

    return resp

########################### Tenant and Logo Information #########################
def get_tenants(orgId):
    url = BASE_API_URL + f'/api/v2/tenants/{orgId}/clients/minimal'
    res = get_response(url, 'V2 Tenants')
    logger.info('Get tenants API response is %s', res)
    if res == None or not res.ok:
        logger.error('Get tenants API is failed')
    return res.json()


def get_tenant_list(org_id, level, tenant_list):
    tenant_id_list = []
    if level == 'partner':
        tenant_id_list.append(org_id)
    elif level == 'all-clients':
        tenants = get_tenants(org_id)
        for tenant in tenants:
            tenant_id_list.append(tenant['uniqueId'])
    elif level == 'specific_clients':
        for tenant in tenant_list:
            tenant_id_list.append(tenant['uniqueId'])
    else:
        tenant_id_list.append(org_id)
    return tenant_id_list


    
def prepare_tenant_list(form, parameters, all_clients=False):
    tenant_id_list = []
    if parameters is not None and len(parameters) > 0:
        if 'allClients' in parameters and (parameters['allClients'] == True or parameters['allClients'] == 'true'):
            tenant_id_list = fetch_all_clients(form.get_tenant_id(), form.get_tenant_context(), all_clients)
        elif 'client' in parameters and parameters['client'] is not None:
            clients = parameters['client']
            if clients == 'All Clients' or clients == 'All Client' or clients == ['All Clients']:
                tenant_id_list = fetch_all_clients(form.get_tenant_id(), form.get_tenant_context(), all_clients)
            else:
                if isinstance(clients, list):
                    tenant_id_list = clients
                else:
                    for i in clients.split(','):
                        tenant_id_list.append(i)
        else:
            tenant_id_list = fetch_all_clients(form.get_tenant_id(), form.get_tenant_context(), all_clients)
    else:
        tenant_id_list = fetch_all_clients(form.get_tenant_id(), form.get_tenant_context(), all_clients)
    return tenant_id_list



def fetch_all_clients(tenant_id, context, all_clients):
    tenant_id_list = []
    if all_clients and context == 'partner':
        context = 'all-clients'
    tenant_id_list = get_tenant_list(tenant_id, context, None)
    return tenant_id_list



def get_tenant_info(tenant_id_list, keys):
    tenant_info = []
    for tenant_id in tenant_id_list:
        info={}
        url = BASE_API_URL + f'/tenancy/api/v7/tenants/{tenant_id}/getTenant'
        res = get_response(url, f'V7 tenants, tenant id is : {tenant_id}')
        if res == None or not res.ok:
            logger.error('Get tenant info API is failed')
            return tenant_info
        else:
            for key in keys:
                info[key] = res.json()[key]
            tenant_info.append({tenant_id: info})
    return tenant_info



def get_logo_path_url(id):
    url = BASE_API_URL + f'/api/v2/tenants/{id}/customBranding?cascade=true'
    res = get_response(url, f'V2 tenants logo, tenant id is : {id}')
    if res == None or not res.ok:
        logger.error('Get logo path url API is failed')
        return ''
    if ('logo' in res.json() and res.json()['logo']) and ('logoPath' in res.json()['logo'] and res.json()['logo']['logoPath']):
        return res.json()['logo']['logoPath']
    else:
        logger.error('Get logo path url is empty')
        return ''



def get_app_logo(id, context, parameters):
    if context == 'client':
        return get_logo_path_url(id)
    elif context == 'partner':
        if parameters is not None and len(parameters) > 0:
            if 'allClients' in parameters and (parameters['allClients'] == True or parameters['allClients'] == 'true'):
                return get_logo_path_url(id)
            elif 'client' in parameters and parameters['client'] is not None:
                clients = parameters['client']
                if clients == 'All Clients' or clients == 'All Client' or clients == ['All Clients']:
                    return get_logo_path_url(id)
                else:
                    if isinstance(clients, list):
                        if len(clients) == 1:
                            for cid in clients:
                                return get_logo_path_url(cid)
                        else:
                            return get_logo_path_url(id)
                    else:
                        return get_logo_path_url(clients) 
    return get_logo_path_url(id)


def update_run_progress(tenant_id, run_id, percent, message):
    url = BASE_API_URL + f'/reporting/api/v3/tenants/{tenant_id}/runs/{run_id}/progress'
    data = {
        "runningPercentage" : percent
    }
    res = call_put_requests(url , data=json.dumps(data), verify=False);
    if res == None or not res.ok:
        logger.error('Update run progress API is failed')
        return res
    else:
        logger.error('Update run progress result updated upto %d',  percent)
        return res
    #TODO : Implement logic here to update the run