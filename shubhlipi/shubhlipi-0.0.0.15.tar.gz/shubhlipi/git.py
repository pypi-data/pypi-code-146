import requests
from requests import get, post
import mimetypes
from .file import read_bin


def upload_release_file(
    file,
    repo,
    tag,
    token,
    dlt=True,
    upld=True,
    fl_type=None,
    fl_data=None,
    log=True,
):
    if log:
        print("Current File: ", file)
    file_name = file.split("\\").split("/")[-1].replace(" ", ".")
    rq = get(
        "https://api.github.com/repos/" + repo + "/releases",
        headers={
            "Authorization": "token " + token,
        },
    )
    if log:
        print("initial response code: " + str(rq.status_code))
    tag_id = ""
    t = 1
    for x in rq.json():
        if x["tag_name"] == tag:
            tag_id = x["id"]
            t = x
            break
    rq.close()
    if log:
        print("Current Release id:", tag_id if tag_id != "" else "File Not Found")
    main = t
    file_id = ""
    for x in main["assets"]:
        if x["name"] == file_name:
            file_id = x["id"]
    if log:
        print("Current File id:", file_id if file_id != "" else "File Not Found")
    upload_url = main["upload_url"].replace("{?name,label}", "")

    def del_file(id):
        rq = requests.delete(
            f"https://api.github.com/repos/{repo}/releases/assets/{id}",
            headers={"Authorization": "token " + token},
        )
        print("File Delete Response:", rq.status_code)
        rq.close()

    def upload_asset(file_type, file_data):
        if file_type is None:
            file_type = mimetypes.guess_type(file)[0]
            if file_type is None:
                file_type = "application/octet-stream"
        rq = post(
            upload_url,
            headers={
                "Authorization": "token " + token,
                "Content-Type": file_type,
            },
            params={"name": file_name},
            data=read_bin(file) if file_data is None else file_data,
        )
        if log:
            print("Upload Response:", rq.status_code)
        rq.close()

    if dlt and file_id != "":
        del_file(file_id)
    if upld and tag_id != "":
        upload_asset(fl_type, fl_data)


def make_release_tag(lnk, tg, token, log=True, **args):
    rq = post(
        f"https://api.github.com/repos/{lnk}/releases",
        headers={"Authorization": "token " + token},
        json={"tag_name": tg} | args,
    )
    if log:
        print("Release Creation Response: ", rq.status_code)
    rq.close()


def delete_release_tag(lnk, tg, token, log=True):
    rq = get(
        "https://api.github.com/repos/" + lnk + "/releases",
        headers={
            "Authorization": "token " + token,
        },
    )
    tag_id = ""
    for x in rq.json():
        if x["tag_name"] == tg:
            tag_id = x["id"]
            break
    rq.close()
    if tag_id == "":
        if log:
            print("Release Not found")
        return
    else:
        if log:
            print("Release id:", tag_id)
    rq = requests.delete(
        f"https://api.github.com/repos/{lnk}/releases/{tag_id}",
        headers={"Authorization": "token " + token},
    )
    if log:
        print("Release Deletion Response: ", rq.status_code)
    rq.close()
