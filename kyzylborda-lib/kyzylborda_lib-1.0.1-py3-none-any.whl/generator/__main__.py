import argparse
import importlib
import json
import os
import sys

from ..secrets import get_flag, get_secret, get_token
from ..secrets.autodetect import load_manifest


def main():
    parser = argparse.ArgumentParser(prog="kyzylborda_lib.generator")
    parser.add_argument("module_name")
    parser.add_argument("user_id")
    parser.add_argument("target_dir")
    parser.add_argument("tasks")  # TODO: handle multiple tasks
    args = parser.parse_args()

    task_name = args.tasks

    os.environ["KYZYLBORDA_ATTACHMENTS_DIR"] = os.path.join(args.target_dir, "attachments")
    os.environ["KYZYLBORDA_USER_ID"] = args.user_id
    os.environ["TASK_NAME"] = task_name

    if args.module_name:
        module = importlib.import_module(args.module_name)
    else:
        module = None

    manifest = load_manifest()

    result = None
    if module and hasattr(module, "generate"):
        result = module.generate()
    if result is None:
        result = {}

    if "flags" not in result:
        result["flags"] = [get_flag()]

    if "urls" not in result:
        result["urls"] = []
    if hasattr(module, "URLS"):
        result["urls"] += module.URLS

    if manifest is not None and manifest.get("daemon", {}).get("socket_type") == "http":
        result["urls"].append(f"https://{task_name}.{{hostname}}/{get_token()}")

    if "substitutions" not in result:
        result["substitutions"] = {}

    if manifest is not None and "kyzylborda-lib-quarantine-daemon" in manifest.get("daemon", {}).get("exec", ""):
        result["substitutions"]["reboot_machine"] = f"""
            <p>
                <small>Сервер этой задачи запущен в отдельном контейнере для вашей команды.</small>
            </p>
            <form method="POST">
                <button>Перезапустить контейнер</button>
            </form>
            <script>
                Array.from(document.querySelectorAll("form")).slice(-1)[0].action = location.protocol + "//{task_name}." + location.host + "/__internal__/reboot_container/{get_token()}?" + location.href;
            </script>
        """

    if manifest is not None and "secrets" in manifest:
        for secret_name in manifest["secrets"]:
            if secret_name != "seed":
                result["substitutions"][secret_name] = get_secret(secret_name)
    try:
        result["substitutions"]["token"] = get_token()
    except ValueError:
        pass

    json.dump(result, sys.stdout)


if __name__ == "__main__":
    main()
