import traceback
import sys
import logging
from dateutil.relativedelta import *
import json
import jwt  # pipenv install pyjwt
import jsonpickle
import boto3
from Crypto.Cipher import AES  # pipenv install pycryptodome
from Crypto import Random
from datetime import datetime
import base64
import os

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
lambda_client = boto3.client("lambda")


class Common:
    VARIABLE_BODY = "body"
    VARIABLE_JWT_NATIVE = "jwt_native"
    VARIABLE_JWT_CUSTOM = "jwt_custom"
    VARIABLE_QUERY = "query"
    VARIABLE_DIRECT = "direct"
    VARIABLE_PARAMETER = "param"
    VARIABLE_JWT_TOKEN = "jwt_token"
    START = None

    def __init__(self) -> None:
        pass

    def start_counter():
        Common.START = datetime.now()

    def runtime():
        return round((datetime.now() - Common.START).total_seconds() * 1000, 2)

    # To call the Lambda function asynchronously, use invokcation_type=Event
    def invoke_lambda(function_name, payload, invocation_type="RequestResponse"):

        # logger.info(f"Started invoking lambda function = {function_name} with invocation type = {invocation_type} of "
        #             f"event payload = {payload}")

        response = lambda_client.invoke(FunctionName=function_name, InvocationType=invocation_type, Payload=json.dumps(payload))
        if invocation_type == "RequestResponse":
            return_response = json.loads(response["Payload"].read())
        else:
            return_response = response["ResponseMetadata"]

        return return_response

    def log(logger, event, context, safe_to_log_override={}):
        # Don't log if it's a ping
        if Common.get_parameter(event, "ping", Common.VARIABLE_DIRECT):
            return True

        safe_to_log = {}
        safe_to_log["fiscal_year"] = True
        safe_to_log["requested_data"] = True
        safe_to_log["start_date"] = True
        safe_to_log["end_date"] = True
        safe_to_log["id"] = True

        safe_to_log.update(safe_to_log_override)
        # logger.info('## ENVIRONMENT VARIABLES\r' +
        #             jsonpickle.encode(dict(**os.environ)))
        logged_event = Common.recoursive_clean(event, None, safe_to_log)
        logger.info("## EVENT\r" + jsonpickle.encode(logged_event))
        logger.info("## CONTEXT\r" + jsonpickle.encode(context))

    def recoursive_clean(obj, key, safe_to_log):
        if isinstance(obj, dict):
            return {k: Common.recoursive_clean(v, k, safe_to_log) for k, v in obj.items()}
        elif isinstance(obj, list):
            return [Common.recoursive_clean(v, key, safe_to_log) for v in obj]
        elif (key in safe_to_log and safe_to_log[key]) or (key.strip().lower().endswith("id") and key not in safe_to_log):
            return obj
        elif obj is not None and (isinstance(obj, bool) or (isinstance(obj, str) and (obj.strip().lower() == "yes" or obj.strip().lower() == "no"))):
            return obj
        elif obj is None:
            return None
        elif obj is not None and isinstance(obj, str) and (obj.strip() == ""):
            return ""
        else:
            return "?"

    def handle_errors(context):
        region = context.invoked_function_arn.split(":")[3]
        aws_account_id = context.invoked_function_arn.split(":")[4]
        exception_type, exception_value, exception_traceback = sys.exc_info()
        traceback_string = traceback.format_exception(exception_type, exception_value, exception_traceback)
        err_msg = json.dumps(
            {
                "function_name": context.function_name,
                "errorType": exception_type.__name__,
                "errorMessage": str(exception_value),
                "stackTrace": traceback_string,
                "log_group_name": context.log_group_name,
                "log_stream_name": context.log_stream_name,
                "request id": context.aws_request_id,
            }
        )
        logger.error(err_msg)

        if str(exception_type) == "<class 'ValueError'>":
            return_value = {
                "StatusCode": 400,
                "ErrorMessage": str(exception_value),
            }
        else:
            try:
                sns_client = boto3.client("sns")
                sns_client.publish(
                    TargetArn=f"arn:aws:sns:{region}:{aws_account_id}:system-errors", Message=json.dumps({"default": err_msg}), MessageStructure="json"
                )
            except Exception as e:
                pass

            return_value = {
                "StatusCode": 500,
                "ErrorMessage": str(exception_value),
            }

        return return_value

    def get_ssm_value(ssm, key):
        value = ssm.get_parameter(Name=key, WithDecryption=True)["Parameter"]["Value"]

        return value

    def write_ssm_value(ssm, key, value, description="", override=True):
        response = ssm.put_parameter(Name=key, Description=description, Value=value, Type="SecureString", Overwrite=override, DataType="text")
        return response

    def send_message_to_queue(sqs, queue_url, dict_message_properties):
        """
        Adds a new SQS item to re-invoke the Lambda for the next page.
        """
        message_attributes = {}
        for key, value in dict_message_properties.items():
            message_attributes[key] = {"DataType": "String", "StringValue": value}

        response = sqs.send_message(QueueUrl=queue_url, DelaySeconds=0, MessageAttributes=message_attributes, MessageBody=(f"Pushed to SQS"))

        return response

    def send_slack_message(channel, message, emoji=":tada:"):
        slack_payload = {"channel": channel, "message": message, "emoji": emoji}

        Common.invoke_lambda("slack-client", slack_payload)

    def get_info_from_jwt(event, parameter):
        headers = event.setdefault("headers", "")
        parameter_value = None
        if headers != "":
            jwt_string = headers.setdefault("authorization", "").replace("Bearer", "").replace("bearer", "").strip()
            if jwt_string != "":
                jwt_info = jwt.decode(jwt_string, options={"verify_signature": False})
                parameter_value = jwt_info[parameter]

        return parameter_value

    def get_body_as_object(event):
        body_as_object = {}
        try:
            if "body" in event:
                if isinstance(event["body"], str):
                    body_as_object = json.loads(event["body"])
                else:
                    body_as_object = event["body"]
        except Exception:
            pass

        return body_as_object

    def get_parameter(event, parameter, type, default_value=None, json_load=False):
        parameter_value = default_value

        event_body = Common.get_body_as_object(event)

        if type == Common.VARIABLE_BODY:
            parameter_value = event_body.get(parameter, default_value)
        elif type == Common.VARIABLE_DIRECT:
            parameter_value = event.setdefault(parameter, default_value)
        elif type == Common.VARIABLE_JWT_CUSTOM:
            headers = event.setdefault("headers", "")
            jwt_string = headers.setdefault("authorization", default_value).replace("Bearer", "").replace("bearer", "").strip()
            if jwt_string != "":
                jwt_info = jwt.decode(jwt_string, options={"verify_signature": False})
                parameter_value = jwt_info[parameter]
        elif type == Common.VARIABLE_JWT_TOKEN:
            headers = event.setdefault("headers", "")
            jwt_string = headers.setdefault("authorization", default_value).replace("Bearer", "").replace("bearer", "").strip()
            parameter_value = jwt_string
        elif type == Common.VARIABLE_JWT_NATIVE:
            parameter_value = event["requestContext"]["authorizer"]["jwt"]["claims"][parameter]
        elif type == Common.VARIABLE_PARAMETER:
            pathParameters = event.setdefault("pathParameters", None)
            if pathParameters != None:
                parameter_value = pathParameters.setdefault(parameter, default_value)
        elif type == Common.VARIABLE_QUERY:
            querystring = event.setdefault("queryStringParameters", None)
            if querystring != None:
                parameter_value = querystring.setdefault(parameter, default_value)

        if json_load:
            if parameter_value == None:
                parameter_value = {}
            else:
                parameter_value = json.loads(parameter_value)

        return parameter_value

    def encrypt(key, string_to_encrypt):
        """
        NOTE: The key has to be 16, 32, 48, 128 characters in size

        Retursn a base64 encoded string as a string
        """
        key = bytes(key, "utf-8")
        string_to_encrypt_bytes = string_to_encrypt.encode()
        iv = Random.new().read(AES.block_size)
        cipher = AES.new(key, AES.MODE_CFB, iv)
        msg = iv + cipher.encrypt(string_to_encrypt_bytes)
        msg = base64.b64encode(msg).decode("utf-8")
        # encrypted = msg.encode("hex")
        return msg

    def decrypt(key, string_to_decrypt):
        """
        Accepts the output of the encrypt method (base64 encoded string)
        Returns the decrypted data as a string
        """
        string_to_decrypt = base64.b64decode(string_to_decrypt)
        key = bytes(key, "utf-8")
        cipher = AES.new(key, AES.MODE_CFB, string_to_decrypt[:16])
        decrypted = cipher.decrypt(string_to_decrypt[16:])
        return decrypted.decode()

    def get_company_info_and_model(psql, jwt_claims, company_hashid):
        email = jwt_claims["https://serenity.sabi.ai/email"]
        model = psql(
            os.environ["hashid_salt"],
            os.environ["db_host"],
            os.environ["db_user"],
            os.environ["db_password"],
            os.environ["clients_db"],
            os.environ["clients_db_schema"],
            os.environ["db_port"],
        )

        company_info = model.get_schema_by_email_and_company_hashid(email, company_hashid)
        model = psql(
            os.environ["hashid_salt"],
            os.environ["db_host"],
            os.environ["db_user"],
            os.environ["db_password"],
            os.environ["clients_db"],
            company_info[0]["schema_name"],
            os.environ["db_port"],
            company_info[0]["timezone"],
        )

        return company_info, model
