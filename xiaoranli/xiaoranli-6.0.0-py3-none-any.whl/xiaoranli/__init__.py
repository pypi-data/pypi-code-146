import os
from termcolor import cprint
import fire
import xiaoranli as pkg


pkg_installed_path = pkg.__path__[0]


def setup_rc_files(dry_run=True):
    """dry_run can be True or False"""
    assert isinstance(dry_run, bool), "dry_run should be a boolean, so its value can only by True or False"
    rc_files_path = os.path.join(pkg_installed_path, "data/rc_files")
    if dry_run:
        cprint("use '--dry_run=False' to disable dry run", "red")
    for root, dirs, files in os.walk(rc_files_path):
        for f in files:
            rc_file = os.path.join(root, f)
            dst = f"~/.{f}"
            if dry_run:
                print(f"in dry run, backup {dst} and copy {rc_file} to {dst}")
            else:
                cmd = f"sudo HOME=$HOME bash -c 'cp {dst} {dst}.backup; cp {rc_file} {dst}'"
                print(cmd)
                os.system(cmd)
    # os.system("sudo HOME=$HOME bash -c 'cat ~/.alias >> ~/.zshrc' ")


def setup_zshrc():
    os.system("sudo HOME=$HOME bash -c 'cat ~/.alias >> ~/.zshrc' ")


def install_zsh():
    zsh_path = os.path.join(pkg_installed_path, "scripts/install_zsh.sh")
    os.system(f"bash {zsh_path}")


def install_golang():
    zsh_path = os.path.join(pkg_installed_path, "scripts/install_zsh.sh")
    os.system(f"bash {zsh_path}")


def install_packages():
    scripts_path = os.path.join(pkg_installed_path, "scripts/install_useful_tools.sh")
    os.system(f"bash -i {scripts_path}")


def info():
    """print help info"""
    cprint(
        "1. if you want tab completion, please 'xiaoranli -- --completion > ~/.xiaoranli; echo source  ~/.xiaoranli >> ~/.bashrc'",
        "red",
    )
    cprint(
        f"2. there are many shell scripts in {os.path.join(pkg_installed_path, 'scripts')}, you could modify PATH to make them as command shell command",
        "red",
    )
    cprint(
        "3. you could also use 'xiaoranli zsh' to install zsh,then use 'xiaoranli tools' to install packages, then use 'xiaoranli rc' to setup rc files",
        "red",
    )


def main():
    fire.Fire(
        {
            "rc": setup_rc_files,
            "info": info,
            "zsh": install_zsh,
            "tools": install_packages,
        }
    )


if __name__ == "__main__":
    main()
