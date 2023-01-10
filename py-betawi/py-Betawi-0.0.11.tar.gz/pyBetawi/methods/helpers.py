import asyncio
import importlib
import os
import ssl
import sys

from geezlibs import Client
from ..pyrogram import eor, section
from ..Clients import *

from .func import run_async


try:
    import certifi
except ImportError:
    certifi = None


try:
    from git import Repo
    from git.exc import GitCommandError, InvalidGitRepositoryError, NoSuchPathError
except ImportError:
    Repo = None


try:
    import heroku3
except ImportError:
    heroku3 = None


class Helpers(object):
    def import_module(
        self,
        path: str,
        exclude: list = [],
        display_module: bool = True
    ):
    
        listbin = []
        listbin.clear()
    
        if not os.path.exists(path):
            return print(f"No path found: {path}")
    
        modules = []
        modules.clear()
    
        for x in os.listdir(path):
            if x.endswith(".py"):
                if x not in ["__pycache__", "__init__.py"]:
                    modules.append(x.replace(".py", ""))
    
        py_path_raw = ".".join(path.split("/"))
        py_path = py_path_raw[0:len(py_path_raw) - 1]
    
        count = 0
        for x in modules:
            if x not in exclude:
                importlib.import_module(py_path + "." + x)
                count += 1
                listbin.append(x)
    
        if display_module:
            data = sorted(listbin)
            for x in data:
                print(x + " Loaded !")
        return count


    async def get_paste(
        self,
        data: str,
        extension: str = "txt"
    ):
        ssl_context = ssl.create_default_context(cafile=certifi.where())
        json = {"content": data, "extension": extension}
        key = await self.async_searcher(
            url="https://spaceb.in/api/v1/documents/",
            json=json,
            ssl=ssl_context,
            post=True,
            re_json=True,
        )
        try:
            return True, key["payload"]["id"]
        except KeyError:
            if "the length must be between 2 and 400000." in key["error"]:
                return await self.get_paste(data[-400000:], extension=extension)
            return False, key["error"]
        except Exception as e:
            print(e)
            return None, str(e)

    async def install_requirements(self):
        try:
            process = await asyncio.create_subprocess_shell(
                " ".join([sys.executable, "-m", "pip", "install", '-U', "-r", "requirements.txt"]),
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
            )
            await process.communicate()
            return process.returncode
        except Exception as e:
            return repr(e)
    
    @run_async
    def gen_chlog(self, repo, diff):
        """Generate Changelogs..."""
        from pyBetawi import geez_ver
        
        UPSTREAM_REPO_URL = (
            Repo().remotes[0].config_reader.get("url").replace(".git", "")
        )
        ac_br = repo.active_branch.name
        ch_log = tldr_log = ""
        ch = f"<b>Geez Pyro Ubot {geez_ver} updates for <a href={UPSTREAM_REPO_URL}/tree/{ac_br}>[{ac_br}]</a>:</b>"
        ch_tl = f"Geez Pyro Ubot {geez_ver} updates for {ac_br}:"
        d_form = "%d/%m/%y || %H:%M"
        for c in repo.iter_commits(diff):
            ch_log += f"\n\n# <b>{c.count()}</b> 🗓 <b>[{c.committed_datetime.strftime(d_form)}]</b>\n<b><a href={UPSTREAM_REPO_URL.rstrip('/')}/commit/{c}>[{c.summary}]</a></b> 👨‍💻 <code>{c.author}</code>"
            tldr_log += f"\n\n# {c.count()} 🗓 [{c.committed_datetime.strftime(d_form)}]\n[{c.summary}]{c.author}"
        if ch_log:
            return str(ch + ch_log), str(ch_tl + tldr_log)
        return ch_log, tldr_log
    
    async def updater(self):
        from .. import logs

        try:
            off_repo = Repo().remotes[0].config_reader.get("url").replace(".git", "")
        except Exception as er:
            logs.exception(er)
            return
        try:
            repo = Repo()
        except NoSuchPathError as error:
            logs.info(f"`directory {error} is not found`")
            Repo().__del__()
            return
        except GitCommandError as error:
            logs.info(f"`Early failure! {error}`")
            Repo().__del__()
            return
        except InvalidGitRepositoryError:
            repo = Repo.init()
            origin = repo.create_remote("upstream", off_repo)
            origin.fetch()
            repo.create_head("main", origin.refs.main)
            repo.heads.main.set_tracking_branch(origin.refs.main)
            repo.heads.main.checkout(True)
        ac_br = repo.active_branch.name
        try:
            repo.create_remote("upstream", off_repo)
        except Exception as er:
            logs.info(er)
        ups_rem = repo.remote("upstream")
        ups_rem.fetch(ac_br)
        changelog, tl_chnglog = await self.gen_chlog(repo, f"HEAD..upstream/{ac_br}")
        return bool(changelog)
    
    async def restart(xd=None):
        from pyBetawi import logs
        
        if Var.HEROKU_APP_NAME and Var.HEROKU_API:
            try:
                Heroku = heroku3.from_key(Var.HEROKU_API)
                app = Heroku.apps()[Var.HEROKU_APP_NAME]
                if xd:
                    await xd.edit("`Restarting your app, please wait for a minute!`")
                app.restart()
            except BaseException as er:
                if xd:
                    return await eor(
                        xd,
                        "`HEROKU_API` or `HEROKU_APP_NAME` is wrong! Kindly re-check in config vars.",
                    )
                logs.exception(er)
        else:
            if len(sys.argv) == 1:
                os.execl(sys.executable, sys.executable, "-m", "pyBetawi")
            else:
                os.execl(
                    sys.executable,
                    sys.executable,
                    "-m",
                    "pyBetawi",
                    sys.argv[1],
                    sys.argv[2],
                    sys.argv[3],
                    sys.argv[4],
                    sys.argv[5],
                    sys.argv[6],
                )
    
    async def get_user_info(self, client: Client, user, already=False):
        if not already:
            user = await client.get_users(user)
        if not user.first_name:
            return ["Deleted account", None]
        user_id = user.id
        username = user.username
        first_name = user.first_name
        mention = user.mention
        dc_id = user.dc_id
        photo_id = user.photo.big_file_id if user.photo else None
        body = {
            "ID": user_id,
            "DC": dc_id,
            "Name": [first_name],
            "Username": [("@" + username) if username else ""],
            "Mention": [mention],
        }
        caption = section("User info", body)
        return [caption, photo_id]


    async def get_chat_info(self, client: Client, chat, already=False):
        if not already:
            chat = await client.get_chat(chat)
        chat_id = chat.id
        username = chat.username
        title = chat.title
        type_ = chat.type
        is_scam = chat.is_scam
        description = chat.description
        members = chat.members_count
        is_restricted = chat.is_restricted
        link = f"[Link](t.me/{username})" if username else "??"
        dc_id = chat.dc_id
        photo_id = chat.photo.big_file_id if chat.photo else None
        body = {
            "ID": chat_id,
            "DC": dc_id,
            "Type": type_,
            "Name": [title],
            "Username": [("@" + username) if username else ""],
            "Mention": [link],
            "Members": members,
            "Scam": is_scam,
            "Restricted": is_restricted,
            "Description": [description],
        }
        caption = section("Chat info", body)
        return [caption, photo_id]
