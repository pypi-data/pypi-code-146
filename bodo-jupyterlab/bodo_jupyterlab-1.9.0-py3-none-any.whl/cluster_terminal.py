import json
from pathlib import Path

from jupyter_server.terminal.api_handlers import TerminalRootHandler
from jupyter_server.terminal.handlers import TermSocket
from jupyter_server.terminal.terminalmanager import TerminalManager
from tornado import web
from jupyter_server.auth import authorized
from jupyter_server._tz import isoformat, utcnow
from jupyter_server.prometheus.metrics import TERMINAL_CURRENTLY_RUNNING_TOTAL
from .ssh_keys_manager import get_cluster_ssh_key_fname
from .config import ALLOW_LOCAL_EXECUTION, BASTION_IP, BASTION_USER

HANDLERS_TO_REMOVE = {TerminalRootHandler, TermSocket}

def remove_default_terminal_handlers(nb_server_app):
    """
    Remove default handlers so we can control the logic on the route
    """
    web_app = nb_server_app.web_app
    for default_router_rule in web_app.default_router.rules:
        rules_idxs_to_delete = []
        for j, target_rule in enumerate(default_router_rule.target.rules):
            if target_rule.target in HANDLERS_TO_REMOVE:
                nb_server_app.log.info(f"Removing {target_rule}")
                rules_idxs_to_delete.append(j)

        # Delete from back to front so indexes don't become corrupted
        for idx in reversed(rules_idxs_to_delete):
            del default_router_rule.target.rules[idx]

def set_terminal_manager(webapp):
    webapp.settings["terminal_manager"] = ClusterTerminalManager(
        shell_command=["/bin/bash"],
        extra_env={
            "JUPYTER_SERVER_ROOT": webapp.settings["server_root_dir"],
            "JUPYTER_SERVER_URL": webapp.settings["base_url"],
        },
        parent=webapp.settings["serverapp"],
    )
    webapp.settings["terminal_manager"].log = webapp.settings["serverapp"].log

class ClusterTerminalManager(TerminalManager):
    def create(self, **kwargs):
        """Create a new terminal.
        Based on https://github.com/jupyter-server/jupyter_server/blob/92c856eea53319fac82971731cc9d208db4861d7/jupyter_server/terminal/terminalmanager.py#L47
        """
        self.log.debug(f"Creating terminal with kwargs: {kwargs}")
        name, term = self.new_named_terminal(**kwargs)
        # Monkey-patch last-activity and cluster, similar to kernels.  Should we need
        # more functionality per terminal, we can look into possible sub-
        # classing or containment then.
        term.last_activity = utcnow()
        if "cluster" in kwargs:
            term.cluster = kwargs["cluster"]

        model = self.get_terminal_model(name)
        # Increase the metric by one because a new terminal was created
        TERMINAL_CURRENTLY_RUNNING_TOTAL.inc()
        # Ensure culler is initialized
        self._initialize_culler()
        return model

    def get_terminal_model(self, name):
        """Return a JSON-safe dict representing a terminal.
        For use in representing terminals in the JSON APIs.
        Based on https://github.com/jupyter-server/jupyter_server/blob/92c856eea53319fac82971731cc9d208db4861d7/jupyter_server/terminal/terminalmanager.py#L89
        """
        self._check_terminal(name)
        term = self.terminals[name]
        model = {
            "name": name,
            "last_activity": isoformat(term.last_activity),
        }

        try:
            model["cluster"] = term.cluster
        except AttributeError:
            pass

        return model


class ClusterTerminalRootHandler(TerminalRootHandler):
    @web.authenticated
    @authorized
    def post(self):
        """POST /terminals creates a new terminal and redirects to it
            Based on https://github.com/jupyter-server/jupyter_server/blob/92c856eea53319fac82971731cc9d208db4861d7/jupyter_server/terminal/api_handlers.py#L26"""
        data = self.get_json_body() or {}

        if "cluster" not in data and not ALLOW_LOCAL_EXECUTION:
            self.set_status(403, "Local terminal forbidden")
            self.finish(json.dumps({"e": "Local terminal forbidden"}))
            return

        # if cwd is a relative path, it should be relative to the root_dir,
        # but if we pass it as relative, it will we be considered as relative to
        # the path jupyter_server was started in
        if "cwd" in data:
            cwd = Path(data["cwd"])
            if not cwd.resolve().exists():
                cwd = Path(self.settings["server_root_dir"]).expanduser() / cwd
                if not cwd.resolve().exists():
                    cwd = None  # type:ignore[assignment]

            if cwd is None:
                server_root_dir = self.settings["server_root_dir"]
                self.log.debug(
                    f"Failed to find requested terminal cwd: {data.get('cwd')}\n"
                    f"  It was not found within the server root neither: {server_root_dir}."
                )
                del data["cwd"]
            else:
                data["cwd"] = str(cwd.resolve())

        if "cluster" in data:
            cluster = json.loads(data["cluster"])
            data["cluster"] = cluster
            ip, uuid = None, None
            try:
                ip = cluster["nodesIp"][0]
                uuid = cluster["uuid"]
            except KeyError as e:
                self.log.debug(f"Missing field in {cluster}: {e}")
                self.set_status(400, "Cluster missing field")
                self.finish(json.dumps({"e": "Cluster missing field"}))
                return

            # Set shell_command to ssh to cluster and escape ip variable since it is untrusted
            if BASTION_IP:
                data["shell_command"] = [
                    "/bin/bash",
                    "-c",
                    f"IP_ESC=$(printf '%q' '{ip}'); ssh -J {BASTION_USER}@{BASTION_IP} bodo@$IP_ESC",
                ]
            else:
                ssh_key_fname = get_cluster_ssh_key_fname(uuid, self.log)
                data["shell_command"] = [
                    "/bin/bash",
                    "-c",
                    f"IP_ESC=$(printf '%q' '{ip}'); ssh -i {ssh_key_fname} $IP_ESC",
                ]
            self.log.info(f"Shell Command: {data['shell_command']}")

        model = self.terminal_manager.create(**data)
        self.finish(json.dumps(model))
