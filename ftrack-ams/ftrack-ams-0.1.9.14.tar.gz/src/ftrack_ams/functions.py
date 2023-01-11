import os

import ftrack_api
from pick import pick


server = "https://ams.ftrackapp.com/api?"


def create_project_name(num, client, name):
    return f"{num}_{client.upper()}_{name.upper()}"


def get_yes_no(question):
    answer = pick(["Yes", "No"], question)
    return True if answer[1] == 0 else False


def get_int_from_user(question):
    while True:
        try:
            intval = int(input(question))
        except ValueError:
            print("Sorry, I didn't understand that? Did you type a number?")
            continue
        else:
            return intval


def clearConsole():
    return os.system("cls" if os.name in ("nt", "dos") else "clear")


def get_ftrack_session():
    return ftrack_api.Session(
        server_url=server,
        api_key=os.getenv("FTRACK_API_KEY"),
        api_user=os.getenv("FTRACK_API_USER"),
    )


def select_artist(team, users, question):
    ia = pick([u["username"] for u in team], question, indicator="👉")
    return [i for i in users if ia[0].lower() in i["username"].lower()][0]


def number_to_letter(input: int) -> str:
    return str(chr(ord("@") + input + 1))


def shotnumber_to_letter(input: int) -> str:
    res = divmod(input, 26)
    quotient = res[0]
    remainder = res[1]
    if quotient > 0:
        return f"{number_to_letter(quotient-1)}{number_to_letter(remainder)}"
    else:
        return number_to_letter(input)


if __name__ == "__main__":
    shotnumber_to_letter(27)
