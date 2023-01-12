"""
utils.py
"""

import os, re, sys, time, json, logging, logging.config
from datetime import datetime

import csv
import boto3
import tempfile
import botocore.exceptions
from botocore.exceptions import NoCredentialsError

global logger
logging.basicConfig(level=logging.INFO)

# BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# LOG_CONF_PATH = os.path.join( BASE_DIR,'..', 'logging.conf')
# LOG_FILE_PATH = os.path.join(BASE_DIR, '..', 'logs', 'cis_automation_'+ datetime.now().strftime('%Y-%m-%d_%H-%M-%S')+ '.log')
# logging.config.fileConfig(LOG_CONF_PATH, defaults={'logfilename': LOG_FILE_PATH})
logger = logging.getLogger('simpleLogger')

# --- Script controls ---

# CIS Benchmark version referenced. Only used in web report.
AWS_CIS_BENCHMARK_VERSION = "1.1"

# Would you like a HTML file generated with the result?
# This file will be delivered using a signed URL.
S3_WEB_REPORT = True

# Where should the report be delivered to?
# Make sure to update permissions for the Lambda role if you change bucket name.
# S3_WEB_REPORT_BUCKET = "CHANGE_ME_TO_YOUR_S3_BUCKET"
S3_WEB_REPORT_BUCKET = "dkumar-cicd"

# Create separate report files?
# This will add date and account number as prefix. Example: cis_report_111111111111_161220_1213.html
S3_WEB_REPORT_NAME_DETAILS = True

# How many hours should the report be available? Default = 168h/7days
S3_WEB_REPORT_EXPIRE = "168"

# Set to true if you wish to anonymize the account number in the report.
# This is mostly used for demo/sharing purposes.
S3_WEB_REPORT_OBFUSCATE_ACCOUNT = False

# Would  you like to send the report signedURL to an SNS topic
SEND_REPORT_URL_TO_SNS = False
SNS_TOPIC_ARN = "CHANGE_ME_TO_YOUR_TOPIC_ARN"

# Would you like to print the results as JSON to output?
SCRIPT_OUTPUT_JSON = True

# Would you like to supress all output except JSON result?
# Can be used when you want to pipe result to another system.
# If using S3 reporting, please enable SNS integration to get S3 signed URL
OUTPUT_ONLY_JSON = False


# def set_globals(self, param_IAM_CLIENT, param_S3_CLIENT):
#     logger.info(" ---Inside utils :: set_globals()--- ")
#     logger.info(" Setting global clients...")
#     # --- Global ---
#     global IAM_CLIENT
#     global S3_CLIENT
#     IAM_CLIENT = param_IAM_CLIENT
#     S3_CLIENT = param_S3_CLIENT


def get_cred_report(self):
    logger.info(" ---Inside utils :: get_cred_report()--- ")
    """Summary

    Returns:
        TYPE: Description
    """
    x = 0
    status = ""
    # global self.session.client('iam')
    cred_report_obj = {}
    try:
        cred_report_obj = self.session.client('iam').generate_credential_report()
        logger.info(f" cred_report_obj: {cred_report_obj} ")
    except botocore.exceptions.ClientError as error:
        logger.error(f" Exception while generate_credential_report(): {error}")

    while cred_report_obj['State'] != "COMPLETE":
        logger.info(" State of self.session.client('iam').generate_credential_report() is not complete")
        time.sleep(2)
        x += 1
        cred_report_obj = self.session.client('iam').generate_credential_report()
        # If no credentail report is delivered within this time fail the check.
        if x > 50:
            status = "Fail: rootUse - no CredentialReport available."
            break
    if "Fail" in status:
        return status
    response = self.session.client('iam').get_credential_report()
    report = []
    # logger.info("resp ", response['Content'])
    reader = csv.DictReader(response['Content'].decode().splitlines(), delimiter=',')
    # logger.info("reader ", reader)
    for row in reader:
        report.append(row)

    # Verify if root key's never been used, if so add N/A
    try:
        if report[0]['access_key_1_last_used_date']:
            pass
    except:
        report[0]['access_key_1_last_used_date'] = "N/A"
    try:
        if report[0]['access_key_2_last_used_date']:
            pass
    except:
        report[0]['access_key_2_last_used_date'] = "N/A"
    return report


def get_account_password_policy(self):
    logger.info(" ---Inside utils :: get_account_password_policy()--- ")
    """Check if a IAM password policy exists, if not return false

    Returns:
        Account IAM password policy or False
    """
    try:
        response = self.session.client('iam').get_account_password_policy()
        return response['PasswordPolicy']
    except Exception as e:
        if "cannot be found" in str(e):
            return False


def get_regions(self):
    logger.info(" ---Inside utils :: get_regions()--- ")
    """Summary

    Returns:
        TYPE: Description
    """

    client = self.session.client('ec2', region_name='us-east-1')
    region_response = {}
    try:
        region_response = client.describe_regions()
    except botocore.exceptions.ClientError as error:
        if error.response['Error']['Code'] == 'AuthFailure':
            logger.error(f" AccessKey credentails not found here: {error}")
            exit(1)
    except botocore.exceptions.NoCredentialsError as e:
        logger.error(f" Unable to locate credentials: {e} ")
        exit(1)

    regions = [region['RegionName'] for region in region_response['Regions']]
    return regions


def get_cloudtrails(self, regions):
    logger.info(" ---Inside utils :: get_cloudtrails()--- ")
    """Summary

    Returns:
        TYPE: Description
    """
    trails = dict()
    for n in regions:
        client = self.session.client('cloudtrail', region_name=n)
        response = client.describe_trails()
        temp = []
        for m in response['trailList']:
            if m['IsMultiRegionTrail'] is True:
                if m['HomeRegion'] == n:
                    temp.append(m)
            else:
                temp.append(m)
        if len(temp) > 0:
            trails[n] = temp
    return trails


def find_in_string(self, pattern, target):
    logger.info(" ---Inside utils :: find_in_string()--- ")
    """Summary

    Returns:
        TYPE: Description
    """
    result = True
    for n in pattern:
        if not re.search(n, target):
            result = False
            break
    return result


def get_account_number(self):
    logger.info(" ---Inside utils :: get_account_number()--- ")
    """Summary

    Returns:
        TYPE: Description
    """
    if S3_WEB_REPORT_OBFUSCATE_ACCOUNT is False:
        client = self.session.client("sts")
        account = client.get_caller_identity()["Account"]
    else:
        account = "111111111111"
    return account


def set_evaluation(self, invokeEvent, mainEvent, annotation):
    logger.info(" ---Inside utils :: set_evaluation()--- ")
    """Summary

    Args:
        event (TYPE): Description
        annotation (TYPE): Description

    Returns:
        TYPE: Description
    """
    configClient = self.session.client('config')
    if len(annotation) > 0:
        configClient.put_evaluations(
            Evaluations=[
                {
                    'ComplianceResourceType': 'AWS::::Account',
                    'ComplianceResourceId': mainEvent['accountId'],
                    'ComplianceType': 'NON_COMPLIANT',
                    'Annotation': str(annotation),
                    'OrderingTimestamp': invokeEvent['notificationCreationTime']
                },
            ],
            ResultToken=mainEvent['resultToken']
        )
    else:
        configClient.put_evaluations(
            Evaluations=[
                {
                    'ComplianceResourceType': 'AWS::::Account',
                    'ComplianceResourceId': mainEvent['accountId'],
                    'ComplianceType': 'COMPLIANT',
                    'OrderingTimestamp': invokeEvent['notificationCreationTime']
                },
            ],
            ResultToken=mainEvent['resultToken']
        )


def json2html(self, controlResult, account):
    logger.info(" ---Inside utils :: json2html()--- ")
    """Summary

    Args:
        controlResult (TYPE): Description

    Returns:
        TYPE: Description
    """
    table = []
    shortReport = shortAnnotation(controlResult)
    table.append(
        "<html>\n<head>\n<style>\n\n.table-outer {\n    background-color: #eaeaea;\n    border: 3px solid darkgrey;\n}\n\n.table-inner {\n    background-color: white;\n    border: 3px solid darkgrey;\n}\n\n.table-hover tr{\nbackground: transparent;\n}\n\n.table-hover tr:hover {\nbackground-color: lightgrey;\n}\n\ntable, tr, td, th{\n    line-height: 1.42857143;\n    vertical-align: top;\n    border: 1px solid darkgrey;\n    border-spacing: 0;\n    border-collapse: collapse;\n    width: auto;\n    max-width: auto;\n    background-color: transparent;\n    padding: 5px;\n}\n\ntable th {\n    padding-right: 20px;\n    text-align: left;\n}\n\ntd {\n    width:100%;\n}\n\ndiv.centered\n{\n  position: absolute;\n  width: auto;\n  height: auto;\n  z-index: 15;\n  top: 10%;\n  left: 20%;\n  right: 20%;\n  background: white;\n}\n\ndiv.centered table\n{\n    margin: auto;\n    text-align: left;\n}\n</style>\n</head>\n<body>\n<h1 style=\"text-align: center;\">AWS CIS Foundation Framework</h1>\n<div class=\"centered\">")
    table.append("<table class=\"table table-inner\">")
    table.append("<tr><td>Account: " + account + "</td></tr>")
    table.append("<tr><td>Report date: " + time.strftime("%c") + "</td></tr>")
    table.append("<tr><td>Benchmark version: " + AWS_CIS_BENCHMARK_VERSION + "</td></tr>")
    table.append(
        "<tr><td>Whitepaper location: <a href=\"https://d0.awsstatic.com/whitepapers/compliance/AWS_CIS_Foundations_Benchmark.pdf\" target=\"_blank\">https://d0.awsstatic.com/whitepapers/compliance/AWS_CIS_Foundations_Benchmark.pdf</a></td></tr>")
    table.append("<tr><td>" + shortReport + "</td></tr></table><br><br>")
    tableHeadOuter = "<table class=\"table table-outer\">"
    tableHeadInner = "<table class=\"table table-inner\">"
    tableHeadHover = "<table class=\"table table-hover\">"
    table.append(tableHeadOuter)  # Outer table
    for m, _ in enumerate(controlResult):
        table.append("<tr><th>" + controlResult[m][0]['ControlId'].split('.')[0] + "</th><td>" + tableHeadInner)
        for n in range(len(controlResult[m])):
            if str(controlResult[m][n]['Result']) == "False":
                resultStyle = " style=\"background-color:#ef3d47;\""
            elif str(controlResult[m][n]['Result']) == "Manual":
                resultStyle = " style=\"background-color:#ffff99;\""
            else:
                resultStyle = " style=\"background-color:lightgreen;\""
            table.append("<tr><th" + resultStyle + ">" + controlResult[m][n]['ControlId'].split('.')[
                1] + "</th><td>" + tableHeadHover)
            table.append("<tr><th>ControlId</th><td>" + controlResult[m][n]['ControlId'] + "</td></tr>")
            table.append("<tr><th>Description</th><td>" + controlResult[m][n]['Description'] + "</td></tr>")
            table.append("<tr><th>failReason</th><td>" + controlResult[m][n]['failReason'] + "</td></tr>")
            table.append("<tr><th>Offenders</th><td><ul>" + str(controlResult[m][n]['Offenders']).replace("', ",
                                                                                                          "',<br>") + "</ul></td></tr>")
            table.append("<tr><th>Result</th><td>" + str(controlResult[m][n]['Result']) + "</td></tr>")
            table.append("<tr><th>ScoredControl</th><td>" + str(controlResult[m][n]['ScoredControl']) + "</td></tr>")
            table.append("</table></td></tr>")
        table.append("</table></td></tr>")
    table.append("</table>")
    table.append("</div>\n</body>\n</html>")
    return table


def s3report(self, htmlReport, account):
    logger.info(" ---Inside utils :: s3report()--- ")
    """Summary

    Args:
        htmlReport (TYPE): Description

    Returns:
        TYPE: Description
    """
    if S3_WEB_REPORT_NAME_DETAILS is True:
        reportName = "cis_report_" + str(account) + "_" + str(datetime.now().strftime('%Y%m%d_%H%M')) + ".html"
    else:
        reportName = "cis_report.html"

    ACCOUNT_NUM = str(account)
    USER_DATA_DIR = os.path.join('data', ACCOUNT_NUM)

    html_path = os.path.join(USER_DATA_DIR, reportName)
    if not os.path.exists(USER_DATA_DIR):
        os.makedirs(USER_DATA_DIR)
        logger.info(" Directory '%s' created" % USER_DATA_DIR)

    logger.info(" Creating HTML report file...")
    with tempfile.NamedTemporaryFile(delete=False) as f, open(html_path, 'a+b') as fp:
        for item in htmlReport:
            f.write(item.encode())
            fp.write(item.encode())
            f.flush()
            fp.flush()
        try:
            f.close()
            fp.close()
            self.session.client('s3').upload_file(f.name, S3_WEB_REPORT_BUCKET, reportName)
            # html_path = os.path.join('data', reportName)
            # os.rename(tempfile,html_path)
            os.unlink(f.name)
        except Exception as e:
            return "Failed to upload report to S3 because: " + str(e)
    ttl = int(S3_WEB_REPORT_EXPIRE) * 60
    signedURL = self.session.client('s3').generate_presigned_url(
        'get_object',
        Params={
            'Bucket': S3_WEB_REPORT_BUCKET,
            'Key': reportName
        },
        ExpiresIn=ttl)
    return signedURL


def json_output(self, controlResult, account):
    logger.info(" ---Inside utils :: json_output()--- ")
    """Summary

    Args:
        controlResult (TYPE): Description

    Returns:
        TYPE: Description
    """
    inner = dict()
    outer = dict()
    for m in range(len(controlResult)):
        inner = dict()
        for n in range(len(controlResult[m])):
            x = int(controlResult[m][n]['ControlId'].split('.')[1])
            inner[x] = controlResult[m][n]
        y = controlResult[m][0]['ControlId'].split('.')[0]
        outer[y] = inner
    if OUTPUT_ONLY_JSON is True:
        logger.debug(json.dumps(outer, sort_keys=True, indent=4, separators=(',', ': ')))
    else:
        logger.debug("JSON output:")
        logger.debug("---------")
        logger.debug(json.dumps(outer, sort_keys=True, indent=4, separators=(',', ': ')))
        logger.debug("---------")
        logger.debug("\n")
        logger.debug("Summary:")
        logger.debug(shortAnnotation(controlResult))
        logger.debug("\n")

    ACCOUNT_NUM = str(account)
    USER_DATA_DIR = os.path.join('data', ACCOUNT_NUM)

    json_path = os.path.join(USER_DATA_DIR, "aws_cis_json_" + ACCOUNT_NUM + ".json")

    if not os.path.exists(USER_DATA_DIR):
        os.makedirs(USER_DATA_DIR)
        logger.info(" Directory '%s' created" % USER_DATA_DIR)

    logger.info(" Creating json report file...")
    try:
        with open(json_path, "w") as fp:
            json.dump(outer, fp, sort_keys=True, indent=4, separators=(',', ': '))
    except Exception as e:
        logger.error(f" Error while writing to JSON file: {e} ")
        exit(1)
    return 0


def shortAnnotation(self, controlResult):
    logger.info(" ---Inside utils :: shortAnnotation()--- ")
    """Summary

    Args:
        controlResult (TYPE): Description

    Returns:
        TYPE: Description
    """
    annotation = []
    longAnnotation = False
    for m, _ in enumerate(controlResult):
        for n in range(len(controlResult[m])):
            if controlResult[m][n]['Result'] is False:
                if len(str(annotation)) < 220:
                    annotation.append(controlResult[m][n]['ControlId'])
                else:
                    longAnnotation = True
    if longAnnotation:
        annotation.append("etc")
        return "{\"Failed\":" + json.dumps(annotation) + "}"
    else:
        return "{\"Failed\":" + json.dumps(annotation) + "}"


def send_results_to_sns(self, url):
    logger.info(" ---Inside utils :: send_results_to_sns()--- ")
    """Summary

    Args:
        url (TYPE): SignedURL created by the S3 upload function

    Returns:
        TYPE: Description
    """
    # Get correct region for the TopicARN
    region = (SNS_TOPIC_ARN.split("sns:", 1)[1]).split(":", 1)[0]
    client = self.session.client('sns', region_name=region)
    client.publish(
        TopicArn=SNS_TOPIC_ARN,
        Subject="AWS CIS Benchmark report - " + str(time.strftime("%c")),
        Message=json.dumps({'default': url}),
        MessageStructure='json'
    )


# returns the list of redShift clusters
def list_redshift_clusters(self, region: str) -> list:
    logger.info(" ---Inside utils :: list_redshift_clusters()---")
    """Summary
    
    Returns:
        TYPE: list
    """

    redshift_clusters = []

    client = self.session.client('redshift', region_name=region)
    marker = ''
    while True:
        if marker == '' or marker is None:
            response = client.describe_clusters()
        else:
            response = client.describe_clusters(
                Marker=marker
            )
        for cluster in response['Clusters']:
            redshift_clusters.append(cluster['ClusterIdentifier'])

        try:
            marker = response['Marker']
            if marker == '':
                break
        except:
            break

    return redshift_clusters


# returns the list of elastic load balancers
def list_elb(self, region: str) -> list:
    logger.info(" ---Inside utils :: list_elb()---")
    """Summary
    
    Returns:
        TYPE: list
    """

    elb_lst = []

    client = self.session.client('elb', region_name=region)
    marker = ''
    while True:
        if marker == '' or marker is None:
            response = client.describe_load_balancers()
        else:
            response = client.describe_load_balancers(
                Marker=marker
            )
        for lb in response['LoadBalancerDescriptions']:
            elb_lst.append(lb['LoadBalancerName'])

        try:
            marker = response['Marker']
            if marker == '':
                break
        except:
            break

    return elb_lst
