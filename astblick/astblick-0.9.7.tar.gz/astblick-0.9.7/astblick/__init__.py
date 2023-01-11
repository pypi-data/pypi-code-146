""" Utility functions for Astblick """

# Copyright (C) 2021 Gwyn Ciesla

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import os
import base64
import datetime
import mimetypes
import html
import getpass
import configparser
import time
import git
import markdown
import cherrypy.process.plugins
from OpenSSL import crypto

def humansize(inbytes):
    """ Convert numeric bytecount to s string in human-readable format """
    suffix = ['B', 'K', 'M', 'G', 'T']
    count = 0
    while inbytes > 1024:
        count = count + 1
        inbytes = inbytes / 1024

    return f"{inbytes:.2f}{suffix[count]}"

def dfree(path):
    """ Get free bytes for a given path: think df """
    fobj = os.statvfs(path)
    space = int(fobj.f_bavail*fobj.f_frsize)

    return space

def cert_expiry(cert):
    """ Get certificate expiration date """
    certfile = open(cert, 'rt', encoding='utf-8').read() # pylint: disable=consider-using-with
    ctx = crypto
    certobj = ctx.load_certificate(ctx.FILETYPE_PEM, certfile)
    expdate = datetime.datetime.strptime(certobj.get_notAfter().decode("utf-8").replace('Z', ''), \
        '%Y%m%d%H%M%S') # pylint: disable=line-too-long
    return str(expdate)

def find_main_branch(repo):
    """ Find primary branch """
    if 'main' in repo.heads:
        return 'main'
    if 'master' in repo.heads:
        return 'master'
    if 'default' in repo.heads:
        return 'default'
    if 'primary' in repo.heads:
        return 'primary'
    return None

def refresh_repos(param, engine, cachedir, clonedir, refresh, refstatfile): # pylint: disable=too-many-locals, too-many-branches, too-many-statements, too-many-arguments
    """ Refresh local clones of configured git repos """
    response = 1
    with engine.connect() as dbconn:
        # pylint: disable=too-many-nested-blocks
        for repoid, reponame, updated, url, key in \
            dbconn.execute("SELECT * FROM repo ORDER by reponame ASC;").fetchall():
            cache = cachedir + '/' + reponame
            clone = clonedir + '/' + reponame
            keylen = len(key)
            if keylen > 0:
                os.environ['GIT_SSH_COMMAND'] = 'ssh -oStrictHostKeyChecking=no -i ' + key
            if (int(datetime.datetime.now().timestamp()) >= updated + int(refresh) \
                or not os.path.isdir(cache)) or param == 'now':
                with open(refstatfile, 'w', encoding='utf-8') as refstat:
                    refstat.write(reponame)
                try:
                    if not os.path.isdir(cache):
                        repo = git.Repo.clone_from(url, cache)
                        repo.remotes.origin.fetch()
                        del repo
                    gdir = git.cmd.Git(cache)
                    # Remove local branches that are gone upstream.
                    gdir.fetch(prune=True)
                    repo = git.Repo(cache)
                    repo.heads[find_main_branch(repo)].checkout()
                    local_branches = []
                    for branch in repo.branches:
                        local_branches.append(branch.name)
                    remote_branches = []
                    for rem_branch in repo.remotes.origin.refs:
                        remote_b = rem_branch.name.split('/')[1]
                        remote_branches.append(remote_b)
                    delete_branches = []
                    for branch in local_branches:
                        if branch not in remote_branches:
                            delete_branches.append(branch)
                    for branch in repo.branches:
                        if branch.name in delete_branches:
                            repo.delete_head(branch, force=True)

                    # Update all remote branches locally, even if new.
                    for ref in repo.remotes.origin.refs:
                        local_b = ref.name.split('/')[1]
                        if local_b not in local_branches and local_b != 'HEAD':
                            new_branch = repo.create_head(local_b)
                            new_branch.set_tracking_branch(ref)
                    for branch in repo.branches:
                        branch.checkout()
                        gdir = git.cmd.Git(cache)
                        gdir.pull()
                        gdir.pull(tags=True)

                    dbconn.execute("UPDATE repo SET updated=" + \
                        str(int(datetime.datetime.now().timestamp()))+ \
                            " WHERE repoid=" + str(repoid) +";")
                    response = "0"
                except git.GitCommandError as exc:
                    print(exc)
                    response = "1"
            if clonedir != cachedir:
                if not os.path.isdir(clone):
                    repo = git.Repo.clone_from(cache, clone)
                    repo.remotes.origin.fetch()
                    del repo
                else:
                    gdir = git.cmd.Git(clone)
                    gdir.pull()
            del os.environ['GIT_SSH_COMMAND']
    with open(refstatfile, 'w', encoding='utf-8') as refstat:
        refstat.truncate()

    return response

def list_cwd(location, clonedir, texttypes, xmltypes):
    # pylint: disable=too-many-branches, too-many-statements, too-many-locals
    """ list files and directories in a given location """
    location = location.replace('..', '')
    dirpath = clonedir + '/' + location
    response = ''
    response = response + "<td valign=top width=15%><table width=100%>"
    loclen = len(location)
    if loclen > 0:
        if location != '/':
            os.chdir(dirpath)
            repo_base = os.popen('git rev-parse --show-toplevel').read().rstrip()
            gdir = git.Repo(repo_base)
            branch_count = len(gdir.branches)
            if branch_count > 1:
                # Form to switch branches
                response = response + "<tr><td>"
                response = response + "<form action=" + cherrypy.request.base + \
                    "><select name=branch>"
                for branch in gdir.branches:
                    if branch.name == gdir.active_branch.name:
                        response = response + "<option value=" + branch.name + \
                            " selected=selected>" + branch.name + "</option>"
                    else:
                        response = response + "<option value=" + branch.name + \
                            ">" + branch.name + "</option>"
                response = response + "</select>"
                response = response + "<input type=hidden name=cwd value=" + location + ">"
                response = response + "<input type=submit value='Switch'></form></td></tr>"
                # Form to view diffs between branches
                response = response + "<tr><td>"
                response = response + "<form action=" + cherrypy.request.base + \
                    "/arbdiff target=_blank><select name=To>"
                for branch in gdir.branches:
                    if branch.name != gdir.active_branch.name:
                        response = response + "<option value=" + branch.commit.hexsha + \
                            ">" + branch.name + "</option>"
                response = response + "</select>"
                response = response + "<input type=hidden name=From value=" + \
                    gdir.active_branch.commit.hexsha + ">"
                response = response + "<input type=hidden name=target value=" + location + ">"
                response = response + "<input type=submit value='Diff'></form></td></tr>"

        response = response + "<tr><th align=left colspan=2>"
        destination = ''
        segref = 0
        for segment in location.split('/'):
            if segref == 0:
                segment = 'root:'
            else:
                segment = '/' + segment
                destination = destination + segment
            response = response + "<a href=" + cherrypy.request.base + \
                "?cwd=" + destination.replace(' ', '%20') + ">" + segment + "</a>"
            segref = segref + 1
        response = response + "</th></tr>"
        if location != '/':
            response = response + "<tr><td>"
            response = response + "<a href=" + cherrypy.request.base + \
                "?cwd=" + os.path.dirname(location).replace(' ', '%20') + ">..</a>"
            response = response + "</td></tr>"
    itemslist = sorted(list(os.listdir(dirpath)))
    itemlist = []
    filelist = []
    for item in itemslist:
        if os.path.isdir(dirpath + '/' + item):
            itemlist.append(item)
        if os.path.isfile(dirpath + '/' + item):
            filelist.append(item)
    for fileob in filelist:
        itemlist.append(fileob)
    for item in itemlist:
        if item not in ['.git', '.astblickrefstat']:
            if os.path.isdir(dirpath + "/" + item):
                if loclen > 0 and location != '/':
                    fill = "/"
                else:
                    fill = ""
                response = response + \
                    "<tr><td style='background-color:#b3b3ff'><a href=" + cherrypy.request.base + \
                    "?cwd=" + location.replace(' ', '%20') + fill + \
                        item.replace(' ', '%20') + ">" + item + "/</a></td><td></td></tr>"
            else:
                displayable = 0
                mime = str(mimetypes.guess_type(dirpath + "/" + item)[0])
                for ftype in texttypes:
                    if ftype in mime and item[-3:] not in xmltypes:
                        displayable = 1
                if displayable == 0:
                    response = response + "<tr>"
                    if 'image' in mime:
                        response = response + \
                            "<td title='Click and hold to view' style='background-color:#e6b3e6'>"\
                                 + item
                        content = base64.b64encode(open(clonedir + location + '/' + item, 'rb').read()).decode('utf-8').replace('\n', '') # pylint: disable=line-too-long,consider-using-with
                        response = response + "<div>"
                        response = response + "<img src='data:" + \
                            mime + f";base64,{content}' />"
                        mime = mime + " " + humansize(len(content))
                        response = response + "</div></td>"
                    else:
                        response = response + "<td style='background-color:#99ff99'>"
                        content = base64.b64encode(open(clonedir + location + '/' + item, \
                            'rb').read()).decode('utf-8').replace('\n', '') # pylint: disable=consider-using-with
                        sixfour = html.escape(content, True)
                        response = response + "<a href='data:" + mime + \
                            f";base64,{sixfour}' download=" + \
                                item + ">" + item + "</a>"
                        response = response + "</td>"
                    response = response + "<td>" + mime + "</td></tr>"
                else:
                    response = response + "<tr><td><a href=" + cherrypy.request.base + \
                        "?display=" + location.replace(' ', '%20') + "/" + \
                            item.replace(' ', '%20') + ">" + item + \
                            "</a></td><td>" + mime + "</td></tr>"

    return response + "</table></td>"

def display_file(filename, clonedir):
    """ Display file contents """
    with open(clonedir + filename, 'r', encoding='utf-8') as c_file:
        if filename.endswith('.md'):
            content = markdown.markdown(c_file.read())
            output = "<td valign=top width=50%><p style='background-color:#ffffb3'>" + \
                filename + "</p><pre>" + \
                    content.replace('<xmp>', '').replace('</xmp>', '') + "</pre></td>"
        else:
            content = c_file.read()
            output = "<td valign=top width=50%><p style='background-color:#ffffb3'>" + \
                filename + "</p><pre><xmp>" + \
                    content.replace('<xmp>', '').replace('</xmp>', '') + "</xmp></pre></td>"
    return output

def format_diff_line(inline):
    """ Color diff lines """

    inline = inline.replace(' ', '&nbsp')

    if inline.startswith('-'):
        bcol = '#ff9999'
    elif inline.startswith('+'):
        bcol = '#99ffbb'
    elif inline.startswith('@@'):
        bcol = '#99d6ff'
    else:
        bcol = 'white'
    return "<tr><td><p style='background-color:" \
        + bcol + "'>" + inline + "</p></td></tr>"

def formdate(commit):
    """ Format dates """
    return datetime.datetime.fromtimestamp(commit.authored_date).strftime('%I:%M %p, %Y-%m-%d') # pylint: disable=line-too-long


def show_history(cwd, display, clonedir): # pylint: disable=too-many-branches, too-many-locals, too-many-statements
    """ Display git history for the current repo """
    target = ''
    if cwd != '':
        bits = cwd.split('/')
        target = bits[1]
    elif display != '':
        bits = display.split('/')
        target = bits[1]

    clone = ''
    if target != '':
        clone = clonedir + "/" + target
        gdir = git.Repo(clone)
        commits = list(gdir.iter_commits())
        tags = gdir.tags
        payload = "<td width=35% valign=top>"
        payload = payload + "<table valign=top>"
        # Form to view arbitrary diffs
        payload = payload + "<tr><th colspan=4>View aggregate differences</th></tr>"
        payload = payload + "<tr><form action=" + cherrypy.request.base + "/arbdiff target=_blank>"
        payload = payload + "<td><select name=From>"
        payload = payload + "<option value='' selected=selected>From</option>"
        for com in commits:
            payload = payload + "<option value=" + com.hexsha + ">" \
                + formdate(com) + " - " + com.hexsha[:7] + "</option>"
        payload = payload + "</select></td>"
        payload = payload + "<td colspan=2><select name=To>"
        payload = payload + "<option value='' selected=selected>To</option>"
        for com in commits:
            payload = payload + "<option value=" + com.hexsha + ">" \
                + formdate(com) + " - " + com.hexsha[:7] + "</option>"
        payload = payload + "</select></td>"
        payload = payload + "<td><input type=hidden name=target value=" + target + ">"
        payload = payload + "<input type=submit value='View Diff'></td>"
        payload = payload + "</form></tr>"

        #Commit history
        payload = payload + "<tr><th>SHA</th><th>Message</th><th>Author</th><th>Commited</th></tr>"
        for commit in commits:
            comtag = ''
            for tag in tags:
                if commit.hexsha == tag.commit.hexsha:
                    comtag = tag.name
            if comtag != '':
                payload = payload + "<tr><th colspan=4>" + comtag + "</th></tr>"
            payload = payload + "<tr>"
            parentlen = len(commit.parents)
            if parentlen > 0:
                payload = payload + "<td><form action=" \
                    + cherrypy.request.base + "/arbdiff target=_blank>"
                payload = payload + "<input type=hidden name=From value=" + \
                    gdir.commit(commit.hexsha + "~1").hexsha + ">"
                payload = payload + "<input type=hidden name=To value=" + commit.hexsha + ">"
                payload = payload + "<input type=hidden name=target value=" + target + ">"
                payload = payload + "<input type=submit value=" + commit.hexsha[:7] + ">"
                payload = payload + "</form></td>"
            else:
                payload = payload + "<td align=center>---</td>"

            payload = payload + "<td>" + str(commit.message) + "</td>"
            payload = payload + "<td>" + str(commit.author) + "</td>"
            payload = payload + "<td>" + str(formdate(commit)) + "</td>"
        payload = payload + "</table></td>"
        del gdir
        return payload

    return "<td valign=top>" + target + "</td>"

def pull_status(engine, clonedir, refresh, refstatfile):
    """ Provide info on status of git refreshing """

    payload = ''
    with engine.connect() as dbconn:
        for reponame, updated in \
            dbconn.execute("SELECT reponame, updated FROM repo ORDER by updated ASC;").fetchall():
            clone = clonedir + '/' + reponame
            if int(datetime.datetime.now().timestamp()) >= updated + 2*(int(refresh)) \
                or not os.path.isdir(clone):
                u_formdate = datetime.datetime.fromtimestamp(updated).strftime('%I:%M %p, %Y-%m-%d')
                payload = payload + "<div style='background-color:#ff9999'>" \
                    + reponame + " not refreshed since " + u_formdate + "!</div>"

    with open(refstatfile, 'r', encoding='utf-8') as refstat:
        status = refstat.read()
    statlen = len(status)
    if statlen > 0:
        payload = payload + \
            "<div style='background-color:#99ffcc'>Refreshing " + status + "...</div>"

    return payload

def homesub(value):
    """ Expand ~ to the full path to the user's home directory. """
    if '~' in value:
        value = value.replace('~',os.path.expanduser('~' + getpass.getuser()))
    return value

def config_handler(configfilename):
    """ Handle creation and reading of the configuration file. """
    database = '~/.astblick.db'
    ipaddr = '127.0.0.1'
    port = 8080
    refresh = '900'
    key = '~/.astblick_key.pem'
    cert = '~/.astblick_cert.pem'
    tempdir = '0'

    if not os.path.isfile(configfilename):
        open(configfilename, 'a', encoding='utf-8').close() # pylint: disable=consider-using-with

    config = configparser.ConfigParser()
    config.read(configfilename)
    sections = config.sections()

    if "Options" not in sections:
        config.add_section("Options")
        config.set("Options", "database", database)
        config.set("Options", "ip", ipaddr)
        config.set("Options", "port", str(port))
        config.set("Options", "refresh", str(refresh))
        config.set("Options", "key", str(key))
        config.set("Options", "cert", str(cert))
        config.set("Options", "tempdir", str(tempdir))
        with open(configfilename, 'w', encoding='utf-8') as config.file:
            config.write(config.file)

    return config

def create_certs(keyf, certf):
    """ Create self-signed certificates """

    # If key doesn't exist, create, otherwise import.
    if not os.path.isfile(keyf):
        key = crypto.PKey()
        key.generate_key(crypto.TYPE_RSA, 4096)
        with open(keyf, 'w', encoding='utf-8') as keyfile:
            keyfile.write(crypto.dump_privatekey(crypto.FILETYPE_PEM, key).decode())
    else:
        with open(keyf, 'r', encoding='utf-8') as keyfile:
            keycontent = keyfile.read()
        key = crypto.load_privatekey(crypto.FILETYPE_PEM, keycontent)

    # If cert exists, return, otherwise create.
    if os.path.isfile(certf):
        return 0

    req = crypto.X509Req()
    req.get_subject().C = 'US'
    req.get_subject().ST = 'None'
    req.get_subject().L = 'None'
    req.get_subject().O = 'None'
    req.get_subject().CN = 'localhost'
    req.set_pubkey(key)
    req.sign(key, "sha256")

    cert = crypto.X509()
    cert.get_subject().CN = 'localhost'
    cert.get_subject().C = 'US'
    cert.get_subject().ST = 'None'
    cert.get_subject().L = 'None'
    cert.get_subject().O = 'None'
    cert.gmtime_adj_notBefore(0)
    cert.gmtime_adj_notAfter(31536000)
    cert.set_issuer(cert.get_subject())
    cert.set_serial_number(int(time.time()))
    cert.set_pubkey(key)
    cert.sign(key, "sha256")

    with open(certf, 'w', encoding='utf-8') as certfile:
        certfile.write(crypto.dump_certificate(crypto.FILETYPE_PEM, cert).decode())

    return 0
