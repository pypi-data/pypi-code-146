"""Spawn Integrated Development Environment."""

import os
import pathlib
import subprocess

HOME = pathlib.Path("~").expanduser()
WORKING = HOME / "code/working"
TUNNEL_SERVER = "159.89.143.168"
# XXX WIDTH = "54"

# TODO CREATE THE TMUX and media pane
# TODO bell inside bangarang (social reader) rings term for mentions


def new_window(title, working_dir, command):
    """Create a new window."""
    pane_id = _create("new-window", "-c", working_dir, "-n", title, "-d", "-P")
    _title_and_run(pane_id, working_dir, command)
    return pane_id


def split_window(reference_pane_id, orientation, quantity, working_dir, command):
    """Split an existing window."""
    quantity_type, _, quantity_size = quantity.partition(" ")
    pane_id = _create(
        "split-window",
        "-c",
        working_dir,
        f"-{orientation}",
        quantity_type,
        quantity_size,
        "-d",
        "-t",
        reference_pane_id,
        "-P",
    )
    _title_and_run(pane_id, working_dir, command)
    return pane_id


def _create(*args):
    """Create a pane using `args` and return its pane id."""
    return (
        subprocess.run(
            ["tmux"] + list(args),
            stdout=subprocess.PIPE,
        )
        .stdout.decode()
        .strip()
    )


def _title_and_run(pane_id, working_dir, command):
    """Title the pane `package` and run `command`."""
    subprocess.run(
        ["tmux", "select-pane", "-t", pane_id, "-T", f" {working_dir.name} "]
    )
    subprocess.run(["tmux", "send-keys", "-t", pane_id, command, "ENTER"])


libs_tools = (
    "canopy",
    "easyuri",
    "gfxint",
    "gmpg",
    "newmath",
    "python-indieauth",
    "python-microformats",
    "python-micropub",
    "python-webmention",
    "sqlyte",
    "txtint",
    "understory",
    "webcli",
    "webint",
)
apps = [
    "auth",
    "code",
    "data",
    "editor",
    "guests",
    "live",
    "media",
    "mentions",
    "owner",
    "posts",
]
sites = (
    "ragt.ag",
    # "1856.house",
    # "indieweb.rocks",
    # "canopy.garden",
)


# XXX def send_keys(*args):
# XXX     return subprocess.run(("tmux", "send-keys") + args)


# XXX def open_pyproject(ref):
# XXX     return send_keys("-t", ref, ":vsp pyproject.toml", "ENTER")


def main():
    """Spawn all windows."""
    # XXX (1) Media
    # XXX ref = new_window("media", HOME, "weechat")
    # XXX split_window(ref, "h", f"-l {WIDTH}", HOME, "ssh pi@family_room")

    # XXX # (1) Libraries & Tools
    # XXX # TODO "mpcli-py", "mpcli-js"
    # XXX ref = new_window("libraries", WORKING / libs_tools[0], "vi -S Session.vim")
    # XXX # XXX open_pyproject(ref)
    # XXX split_window(ref, "h", f"-l {WIDTH}", WORKING, "ls")
    # XXX for lib_tool in libs_tools[1:]:
    # XXX     ref = split_window(
    # XXX         ref,
    # XXX         "v",
    # XXX         "-p 80",
    # XXX         WORKING / lib_tool,
    # XXX         f"vi {lib_tool}/__init__.py",
    # XXX     )
    # XXX     # XXX open_pyproject(ref)

    # XXX # (2) Understory Core
    # XXX ref = new_window("understory", WORKING / "understory", "vi -S Session.vim")
    # XXX # ref = new_window("understory", WORKING / "understory", "vi web/__init__.py")
    # XXX split_window(ref, "h", f"-l {WIDTH}", WORKING / "understory", "ls")
    # XXX # XXX open_pyproject(ref)

    # XXX # (2) Web Applications
    # XXX ref = new_window(
    # XXX     "webapps",
    # XXX     WORKING / f"webint-{apps[0]}",
    # XXX     "vi -S Session.vim",
    # XXX )
    # XXX # XXX open_pyproject(ref)
    # XXX split_window(ref, "h", f"-l {WIDTH}", WORKING, "ls")
    # XXX for app in apps[1:]:
    # XXX     ref = split_window(
    # XXX         ref, "v", "-p 80", WORKING / f"webint-{app}", "vi -S Session.vim"
    # XXX     )
    # XXX     # XXX open_pyproject(ref)

    # XXX # XXX # (3-n) Websites
    # XXX for n, site in enumerate(sites):
    # XXX     port = 4010 + n
    # XXX     tunnel_port = port + 1000
    # XXX     site_name = site.replace(".", "_")
    # XXX     ref = new_window(site, WORKING / site, "vi -S Session.vim")
    # XXX     # XXX ref = new_window(site, WORKING / site, f"vi {site_name}/__init__.py")
    # XXX     # XXX open_pyproject(ref)
    # XXX     split_window(
    # XXX         ref,
    # XXX         "h",
    # XXX         f"-l {WIDTH}",
    # XXX         WORKING / site / site,
    # XXX         f"WEBCTX=dev poetry run web dev {site_name}:app --port {port}",
    # XXX     )
    # XXX     subprocess.run(
    # XXX         [
    # XXX             "ssh",
    # XXX             "-f",
    # XXX             "-N",
    # XXX             "-R",
    # XXX             f"{tunnel_port}:localhost:{tunnel_port}",
    # XXX             f"root@{TUNNEL_SERVER}",
    # XXX         ]
    # XXX     )

    col_libs_tools = new_window("code", WORKING / libs_tools[0], "vi -S Session.vim")
    col_sites = None
    for n, site in enumerate(sites):
        port = 4010 + (n * 10)
        tunnel_port = port + 1000
        site_name = site.replace(".", "_")
        args = [
            WORKING / site / site,
            f"WEBCTX=dev poetry run web dev {site_name}:app"
            f" --port {port} --watch {WORKING}",
        ]
        if n == 0:
            col_sites = split_window(col_libs_tools, "h", "-l 54", *args)
        else:
            split_window(col_sites, "v", "-p 20", *args)
        # subprocess.run(
        #     [
        #         "ssh",
        #         "-f",
        #         "-N",
        #         "-R",
        #         f"{tunnel_port}:localhost:{tunnel_port}",
        #         f"root@{TUNNEL_SERVER}",
        #     ]
        # )
    col_webapps = split_window(
        col_libs_tools, "h", "-l 60", WORKING / sites[0], "vi -S Session.vim"
    )
    for app in reversed(apps):
        split_window(
            col_webapps, "v", "-p 15", WORKING / f"webint-{app}", "vi -S Session.vim"
        )
    for site in reversed(sites[1:]):
        split_window(col_webapps, "v", "-p 15", WORKING / site, "vi -S Session.vim")
    for lib_tool in reversed(libs_tools[1:]):
        split_window(
            col_libs_tools, "v", "-p 15", WORKING / lib_tool, "vi -S Session.vim"
        )


if __name__ == "__main__":
    if os.getenv("TMUX"):
        main()
    else:
        subprocess.run(["tmux", "new", "-x", "200", "-d", "python3", __file__])
