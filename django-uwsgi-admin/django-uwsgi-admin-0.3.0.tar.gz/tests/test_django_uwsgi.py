import os
import re
import subprocess
import time
from pathlib import Path

import psutil as psutil
import requests
from process_tests import TestProcess
from process_tests import dump_on_error
from process_tests import wait_for_strings

TIMEOUT = int(os.getenv('TEST_TIMEOUT', 60))
TEST_PATH = Path(__file__).parent


def test_import():
    from django_uwsgi import panels
    from django_uwsgi import views
    from django_uwsgi import wagtail_hooks

    print(views, panels, wagtail_hooks)


def test_cli(tmp_path: Path):
    tmp_path.cwd()
    subprocess.check_call(['django-admin', 'migrate'])
    subprocess.check_call(['django-admin', 'loaddata', 'test'])
    args = ['uwsgi', f'--ini={TEST_PATH / "uwsgi.ini"}']
    with TestProcess(*args) as process:
        with dump_on_error(process.read):
            wait_for_strings(process.read, TIMEOUT, 'uWSGI http bound')
            t = time.time()
            port = None
            while time.time() - t < TIMEOUT and port is None:
                psprocess = psutil.Process(process.proc.pid)
                for child in psprocess.children():
                    for conn in child.connections('all'):
                        if conn.status == psutil.CONN_LISTEN and conn.laddr[0] == '127.0.0.1':
                            port = conn.laddr[1]
                            break
                    else:
                        continue
                    break
            assert port
            with requests.Session() as session:
                resp = session.get('http://127.0.0.1:%s/admin/' % port)
                (csrftoken,) = re.findall('name=[\'"]csrfmiddlewaretoken[\'"] value=[\'"](.*?)[\'"]', resp.text)
                resp = session.post(
                    'http://127.0.0.1:%s/admin/login/?next=/admin/' % port,
                    data={
                        'csrfmiddlewaretoken': csrftoken,
                        'username': 'test',
                        'password': 'test',
                    },
                )
                assert '<a href="/admin/django_uwsgi/status/">UWSGI Status</a>' in resp.text

                resp = session.get('http://127.0.0.1:%s/admin/django_uwsgi/status/' % port)
                assert '<td>masterpid</td>' in resp.text
