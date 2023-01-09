import json
import os
import platform
import sys
import webbrowser

import requests

import rpu

from .cli import ConsoleClient

client = ConsoleClient()

API_BASE_URL = "https://api.cibere.dev/rpu"
BASE_URL = rpu.__file__.removesuffix("__init__.py")


@client.command(
    name="version",
    description="gives you the version of rpu you are running",
    brief="gives you the version of rpu your using",
    aliases=["v"],
)
def cmd_version():
    print(rpu.__version__)


@client.command(
    name="docs",
    description="opens rpu's documentation. If your using alpha/beta, latest docs will be brought up. If your using final then stable docs will be brought up.",
    brief="opens rpus docs",
    aliases=["d"],
)
def cmd_docs():
    version = "stable" if rpu.version_info.releaselevel == "final" else "latest"

    print(f"Opening the {version} docs in your browser")
    webbrowser.open(f"https://rpu.cibere.dev/{version}/index")


@client.command(
    name="system-info",
    description="gives you system information. Specifically rpu version, python version, and os",
    brief="gives you system info",
    aliases=["os", "s"],
)
def cmd_system_info():
    info = {}

    info["python"] = "v{0.major}.{0.minor}.{0.micro}-{0.releaselevel}".format(
        sys.version_info
    )
    info["rpu"] = "v{0.major}.{0.minor}.{0.micro}-{0.releaselevel}".format(
        rpu.version_info
    )
    info["OS"] = platform.platform()

    nl = "\n"
    print(nl.join([f"{item}: {info[item]}" for item in info]))


@client.command(
    name="install",
    description="lets you install library specific utilities.",
    brief="lets you install library specific utilities",
)
def cmd_install(library_name: str):
    if os.path.isfile(f"{BASE_URL}librarys\\_{library_name}.py"):
        return print(f"Utilities for {library_name} already installed")

    res = requests.get(f"{API_BASE_URL}/get/{library_name}")
    try:
        data = res.json()
    except json.JSONDecodeError:
        return print(f"Unable to convert api response to json\nResponse: {res.text}")
    print("Done making web request")

    if res.status_code == 400:
        return print(data["error"])

    with open(f"{BASE_URL}librarys\\_{library_name}.py", "w") as f:
        f.write(data["code"])
    print("Done creating file")

    with open(f"{BASE_URL}librarys\\__init__.py", "a") as f:
        f.write(f"from . import _{library_name} as {library_name}\n")
    print("Done updating init")
    print(f"\nSuccessfully finished installing utilities for {library_name}.")


@client.command(
    name="uninstall",
    description="lets you uninstall library specific utilities",
    brief="lets you uninstall library specific utilities",
)
def cmd_uninstall(library_name: str):
    fp = f"{BASE_URL}librarys\\_{library_name}.py"
    if not os.path.isfile(fp):
        return print(f"No utilities for {library_name} installed")

    os.remove(fp)
    print("Removed file")

    with open(f"{BASE_URL}librarys\\__init__.py", "r") as f:
        foo = f.read()
    foo = foo.replace(f"from . import _{library_name} as {library_name}", "")
    with open(f"{BASE_URL}librarys\\__init__.py", "w") as f:
        f.write(foo.strip())
    print("Updated init")
    print(f"\nSuccessfully finished uninstalling utilities for {library_name}.")


client.run()
