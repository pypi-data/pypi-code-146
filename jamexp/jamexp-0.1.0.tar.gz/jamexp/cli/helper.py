import typer


def helper():
    cmds = {
        "jcpt": "copy template file from jamexp",
        "jkill": "kill processes using cuda, selected by FZF",
        "jkilla": "kill all processes using cuda",
        "jln": "ln data dir",
        "jjnln": "delte link",
        "jwb_check_running": "check wandb running status",
        "jnb_clean": "clean notebook",
    }
    for key, value in cmds.items():
        print(f"{key:<20}\t\t {value}")


def run_helper():
    typer.run(helper)
