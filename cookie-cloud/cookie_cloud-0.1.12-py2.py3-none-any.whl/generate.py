import re
import os
import json
from os.path import expanduser

conf_path = ".cookie_cloud.json"

TEMPLATE = """
// ==UserScript==
// @name         Get Your Cookie
// @namespace    https://twfb.org
// @version      0.1
// @description  Send your cookies to your github private repo
// @author       twfb
// @match        https://developer.chrome.com/docs/extensions/mv3/
// @grant        GM_xmlhttpRequest
// @grant        GM_cookie
// @grant        GM.cookie
// @connect      api.github.com
//
// ==/UserScript==

const github_user = '';
const github_token = '';
const github_repo = '';


var main_site = document.domain.split('.');
if (main_site.length > 2) {
    main_site = main_site.slice(1, 99).join('.');
} else {
    main_site = main_site.join('.');
}
const issue_title = main_site + ' Cookies';

function git_get(url, fun) {
    console.log("GET ", url)
    return GM_xmlhttpRequest({
        url: url,
        method: 'GET',
        headers: {
            'Accept': 'application/vnd.github.v3+json',
            'Authorization': 'token ' + github_token
        },
        onload: (response) => {
            console.info("Response ", JSON.parse(response.responseText))
            fun(response);
        }
    });
}


function git_delete(url, fun) {
    console.log("DELETE ", url)
    return GM_xmlhttpRequest({
        url: url,
        method: 'DELETE',
        headers: {
            'Accept': 'application/vnd.github.v3+json',
            'Authorization': 'token ' + github_token
        },
        onload: (response) => {
            console.info("Response ", JSON.parse(response.responseText))
            fun(response);
        }
    });
}

function git_post(url, data, fun) {
    console.log("POST ", url, data)
    return GM_xmlhttpRequest({
        url: url,
        method: 'POST',
        headers: {
            'Accept': 'application/vnd.github.v3+json',
            'Authorization': 'token ' + github_token
        },
        data: JSON.stringify(data),
        onload: (response) => {
            console.info("Response ", JSON.parse(response.responseText))
            fun(response);
        }
    });
}

function git_patch(url, data, fun) {
    console.log("PATCH ", url, data)
    return GM_xmlhttpRequest({
        url: url,
        method: 'PATCH',
        headers: {
            'Accept': 'application/vnd.github.v3+json',
            'Authorization': 'token ' + github_token
        },
        data: JSON.stringify(data),
        onload: (response) => {
            console.info("Response ", JSON.parse(response.responseText))
            fun(response);
        }
    });
}

function create_repo(repo, fun) {
    console.log("%cCreate Repo", "background:blue;color:white;padding:5px;border-radius:5px;", repo)
    return git_post('https://api.github.com/user/repos', { "name": repo, "private": true }, fun)
}

function create_issue(repo, title, body, labels, fun) {
    console.log("%cCreate Issue", "background:blue;color:white;padding:5px;border-radius:5px;", repo, title, labels)
    var url = 'https://api.github.com/repos/' + github_user + '/' + repo + '/issues'
    return git_post(url, { title: title, body: body, labels: labels }, function (response) {
        fun(JSON.parse(response.responseText).url);
    })
}

function check_repo(repo, fun) {
    console.log("%cCheck Repo", "background:yellow;color:black;padding:5px;border-radius:5px;", repo)
    var url = 'https://api.github.com/repos/' + github_user + '/' + repo;
    return git_get(url, function (response) {
        if (JSON.parse(response.responseText).id == undefined) {
            create_repo(repo, fun);
        } else {
            fun();
        }
    });
}

function get_or_create_issue(repo, title, body, labels, fun) {
    const url = 'https://api.github.com/repos/' + github_user + '/' + repo + '/issues?labels=' + labels;
    return git_get(url, function (response) {
        var result = JSON.parse(response.responseText);
        if (result[0] == undefined) {
            return create_issue(repo, title, body, labels, fun)
        } else {
            console.log("%cGet Issue", "background:yellow;color:black;padding:5px;border-radius:5px;", result[0].url);
            for (var i = 1; i < result.length; i++) {
                close_issue(result[i].url);
            }
            fun(result[0].url, body);
        }
    });
}

function close_issue(url, fun) {
    console.log("%cClose Issue", "background:yellow;color:black;padding:5px;border-radius:5px;", url);
    const data = { state: 'closed' };
    git_patch(url, data, fun);
}

function create_issue_comment(issue_url, body, fun) {
    console.log("%cCreate Issue Comment", "background:blue;color:white;padding:5px;border-radius:5px;", issue_url);
    return git_post(issue_url + '/comments', { "body": body }, function () {
        fun(issue_url);
    });
}

function delete_issue_comments(issue_url, fun) {
    git_get(issue_url + '/comments?per_page=100', function (response) {
        var comment_list = JSON.parse(response.responseText);
        for (var i = comment_list.length - 2; i > 0; i--) {
            console.log("%cDelete Issue Comment", "background:blue;color:white;padding:5px;border-radius:5px;", comment_list[i].url);
            git_delete(comment_list[i].url, fun);
        }
    })
}

function get_last_comment_body(issue_url, fun){
    return git_get(issue_url + '/comments?per_page=100', function (response) {
        var comment_list = JSON.parse(response.responseText);
        return comment_list[comment_list.length-1].body;
    })
}

function main() {
    console.log("%cUnsubscribe and remove a notification from your inbox? click that link and click \\"Watch\\" or \\"Unwatch\\" then choose \\"Ignore\\".", "background:yellow;color:black;padding:5px;border-radius:5px;", 'https://github.com/' + github_user + '/' + github_repo)
    console.log("%cGet Cookie String", "background:yellow;color:black;padding:5px;border-radius:5px;")
    GM_cookie.list({ url: main_site }, (cookie, error) => {
        check_repo(github_repo, function () {
            get_or_create_issue(github_repo, issue_title, issue_title, [main_site], function (issue_url) {
                create_issue_comment(issue_url, JSON.stringify(cookie), function (issue_url) {
                    delete_issue_comments(issue_url)
                });
            });
        });
    });
}
main();

"""


def main():
    if not os.path.isfile(conf_path):
        json.dump(
            dict(github_user="", github_repo="", github_token="", sites=[]),
            open(conf_path, "w"),
            indent=2,
        )
        print(
            "Generated {} file successed.\nYou can move it to HOME.\nEdit it!".format(
                conf_path
            )
        )
        return
    gyc = TEMPLATE
    conf = json.load(open(conf_path))

    gyc = re.sub(
        "(const github_user =) '.*?'", r"\1 '{}'".format(conf["github_user"]), gyc
    )
    gyc = re.sub(
        "(const github_token =) '.*?'", r"\1 '{}'".format(conf["github_token"]), gyc
    )
    gyc = re.sub(
        "(const github_repo =) '.*?'", r"\1 '{}'".format(conf["github_repo"]), gyc
    )
    sites = map(
        lambda x: "// @match      *://*." + x + "/*\n// @match      *://" + x + "/*\n",
        conf["sites"],
    )
    sites = list(filter(lambda x: x not in gyc, sites))
    gyc = gyc.replace(
        "// ==/UserScript==", "{}// ==/UserScript==".format("".join(sites))
    )
    open("GYC.js", "w").write(gyc)

    print("Generate GYC.js file successed.\nCopy that to your Tampermonkey!")
