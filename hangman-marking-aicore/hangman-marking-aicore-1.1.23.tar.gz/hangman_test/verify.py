import os
import requests
import json

user_id = os.environ['USER_ID']
token = os.environ['API_TOKEN']
url_api = os.environ['API_ROOT']
url_endpoint = url_api + "/user/projects/task/verify"
print(url_endpoint)
headers = {'x-api-key': f"{token}"}

def get_errors_fails(report_path: str):
    with open(report_path, 'r') as f:
        report = f.read()

    list_fails = report.split('======================================================================')

    if len(list_fails) > 1:
        list_fails = list_fails[1:]

    # fail_error = [fail.split('----------------------------------------------------------------------')[0]
    #             for fail in list_fails]
    # print(fail_error)
    
    error_dict = {}

    for error in list_fails:
        if error.startswith('\nERROR'):
            fail_error = error.split('----------------------------------------------------------------------')[0].split('ERROR: ')[1].split(' (')[0]
            message = ' '.join(error.split('----------------------------------------------------------------------')[1].split(': ')[-2:]).strip()
            error_dict[fail_error] = message
        elif error.startswith('\nFAIL'):
            fail_error = error.split('----------------------------------------------------------------------')[0].split('FAIL: ')[1].split(' (')[0]
            message = error.split('----------------------------------------------------------------------')[1].split(' : ')[1].strip()
            if message.endswith("AssertionError:"):
                try: 
                    message = message.split("')")[0]
                except:
                    pass
            error_dict[fail_error] = message

    return error_dict

def mark_complete(task_id: str, message=None):
    data = {
            'taskId': task_id,
            'userId': user_id,
            'verified': True
            }
    if message:
        data['message'] = message
    
    try:
        r = requests.post(url_endpoint, headers=headers, data=json.dumps(data))
        print(f'Marking task {task_id} as complete for user {user_id}')
        print(r.text)
        assert r.status_code == 200
    except Exception as e:
        print(f'Error marking task {task_id} as complete for user {user_id}')
        

def mark_incomplete(task_id: str, message=None):
    data = {
            'taskId': task_id,
            'userId': user_id,
            'verified': False
            }
    if message:
        data['message'] = message
    try:
        r = requests.post(url_endpoint, headers=headers, data=json.dumps(data))
        print(f'Marking task {task_id} as incomplete for user {user_id}')
        print(r.text)
        assert r.status_code == 200
    except:
        print(f'Error marking task {task_id} as incomplete for user {user_id}')

