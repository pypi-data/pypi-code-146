import pickle
import time

import requests
from bs4 import BeautifulSoup
from rich import box
from rich.console import Console
from rich.live import Live
from rich.table import Table
import datetime
import timeago

import uva.localdb as localdb

BASE_URL = 'https://onlinejudge.org'
PDF_FILE_URL = BASE_URL + '/external'

LOGIN_PARAMS = {
    'option': 'com_comprofiler',
    'task': 'login',
}

SUBMIT_PARAMS = {
    'option': 'com_onlinejudge',
    'Itemid': 8,
    'page': 'save_submission'
}

UHUNT_BASE_API_URL = 'https://uhunt.onlinejudge.org/api'
UHUNT_UNAME2UID_API_URL = UHUNT_BASE_API_URL + '/uname2uid'
UHUNT_SUBS_USER_API_URL = UHUNT_BASE_API_URL + '/subs-user'
UHUNT_SUBS_USER_LATEST_API_URL = UHUNT_BASE_API_URL + '/subs-user-last'

NOT_AUTHORIEZED_ERROR_STRING = 'You are not authorised to view this resource'
SUBMISSION_SUCESS_MESSAGE = 'mosmsg=Submission+received+with+ID+'

NOT_LOGGED_IN_MESSAGE = "It's seems that you are not logged in, please login first."


def login(username, password):
    console = Console(log_time=False, log_path=False)
    with console.status("[blue]Logging into uva") as status:
        console.log("Fetching the login form")
        session = requests.Session()
        r = session.get(BASE_URL)
        console.log("Filling out the form")
        soup = BeautifulSoup(r.content, 'html5lib')
        form = soup.find('form', id='mod_loginform')
        inputs = form.find_all('input', type='hidden')

        form_data = {
            'username': username,
            'passwd': password,
            'remember': 'yes'
        }
        for tag in inputs:
            form_data[tag['name']] = tag['value']

        headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
        }

        console.log("Submitting the form")
        # TODO add error checks on this call
        response = session.post(BASE_URL, params=LOGIN_PARAMS, headers=headers, data=form_data)

        res = response.content.decode("utf-8")

        if NOT_AUTHORIEZED_ERROR_STRING in res:
            console.log('You are not authorize')
            return
        elif 'My Account' in res and 'Logout' in res:
            console.log('You are logged in')
        else:
            console.log('There was an error')
            return

        console.log("Saving login token to the local db")
        localdb.save_cookies(pickle.dumps(session.cookies))

        console.log("Getting uva hunt username")
        # TODO add error checking on this call
        p = requests.get(UHUNT_UNAME2UID_API_URL + '/' + username)

        console.log("Saving uva hunt username to local db")
        localdb.save_login_data(username, p.content.decode("utf-8"))
        console.log("[bold green]All done")


def get_latest_subs(count):
    console = Console(log_time=False, log_path=False)
    console.status("[blue]Logging into uva")
    cookie = localdb.read_cookies()
    if cookie is None:
        console.log(NOT_LOGGED_IN_MESSAGE)
        return
    uhunt_uid = localdb.read_uhunt_uid()
    url = f'{UHUNT_SUBS_USER_LATEST_API_URL}/{uhunt_uid}/{count}'
    submissions = requests.get(url)
    return submissions.content.decode("utf-8")


def logout():
    console = Console(log_time=False, log_path=False)
    with console.status("[blue]Logging out from uva") as status:
        localdb.purge()
        console.log("[bold green]All done")


def submit(problem_id, filepath, language):
    console = Console(log_time=False, log_path=False)
    console.status("[blue]Submitting your solution")
    cookie = localdb.read_cookies()
    if cookie is None:
        console.log(NOT_LOGGED_IN_MESSAGE)
        return
    session = requests.session()
    session.cookies.update(pickle.loads(cookie))

    files = {
        'localid': (None, problem_id),
        'language': (None, language),
        'codeupl': (filepath, open(filepath, 'rb')),
    }
    console.log("Uploading solution to Uva")
    response = session.post(BASE_URL, params=SUBMIT_PARAMS, files=files)
    res = response.content.decode("utf-8")

    if NOT_AUTHORIEZED_ERROR_STRING in res:
        console.log(NOT_AUTHORIEZED_ERROR_STRING)
    elif SUBMISSION_SUCESS_MESSAGE in res:
        index = res.find(SUBMISSION_SUCESS_MESSAGE)
        end = res.find('"', index)
        submission_id = res[index + len(SUBMISSION_SUCESS_MESSAGE):end]
        console.log(f"Submission with submission id {submission_id} submitted")
        wait_for_submission_results(submission_id, console)
    else:
        console.log('There was an error')


def wait_for_submission_results(submission_id, console):
    console.log("Waiting for results")
    uhunt_uid = localdb.read_uhunt_uid()
    sub_id = str(int(submission_id) - 1)
    verdict_dict = {
        0: "Processing",
        10: "Submission error",
        15: "Can't be judged",
        20: "In queue",
        30: "Compile error",
        35: "Restricted function",
        40: "Runtime error",
        45: "Output limit",
        50: "Time limit",
        60: "Memory limit",
        70: "Wrong answer",
        80: "PresentationE",
        90: "Accepted"
    }

    language_dict = {
        1: "ANSI C",
        2: "Java",
        3: "C++",
        4: "Pascal",
        5: "C++11",
        6: "Python"
    }

    with Live(console=console, auto_refresh=False) as live:
        while True:
            table = Table(
                "Submission ID", "Problem ID", "Verdict ID", "Runtime", "Submission Time", "Language",
                "Rank", box=box.SIMPLE
            )
            res = requests.get(f"{UHUNT_SUBS_USER_API_URL}/{uhunt_uid}/{sub_id}")
            print(res.json())
            if len(res.json()["subs"]) == 0:
                continue
            s = res.json()["subs"][0]

            submission_time = timeago.format(datetime.datetime.fromtimestamp(s[4]))
            table.add_row(
                str(s[0]),
                str(s[1]),
                verdict_dict[s[2]],
                str(s[3]),
                submission_time,
                language_dict[s[5]],
                str(s[6])
            )
            live.update(table, refresh=True)
            time.sleep(3)


def get_pdf_file(problem_id):
    url = f"{PDF_FILE_URL}/{problem_id[0:3]}/{problem_id}.pdf"
    print(url)
    res = requests.get(url)
    with open(f'{problem_id}.pdf', 'wb') as f:
        f.write(res.content)

