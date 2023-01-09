import click
from click import Abort
from cookiecutter.main import cookiecutter
from shutil import rmtree, unpack_archive
from .usefull_function import multiprocessing_download
from pathlib import Path

__required_options = {
    True: 'modules_dir',
    False: 'scheduler'
}


def __install_cluster(snake_installer, scheduler, env, bash_completion):
    """Run installation of tool for HPC cluster"""
    # rm previous install (ie @julie cluster then local)
    snake_installer.clean_home()
    # build default profile path
    default_profile = snake_installer.default_profile

    # test if install already run
    try:
        if default_profile.exists() and click.confirm(
                click.style(f'    Profile "{default_profile}" exist do you want to remove and continue?\n\n', fg="red"),
                default=False, abort=True):
            rmtree(default_profile, ignore_errors=True)
        default_profile.mkdir(exist_ok=True)

        default_cluster = snake_installer.install_path.joinpath("install_files", f"cluster_config_{scheduler.upper()}.yaml").open(
            "r").read()
        command = r"""sinfo -s | grep "*" | cut -d"*" -f1 """
        default_partition = subprocess.check_output(command, shell=True).decode("utf8").strip()
        if not default_partition:
            click.secho("    Error: Slurm was not found on your system !!", fg="red", err=True)
            snake_installer.fail()
            raise SystemExit
        default_profile.joinpath("cluster_config.yaml").open("w").write(
            default_cluster.replace("PARTITION", default_partition))

        # Download cookiecutter of scheduler
        click.secho(
            f"    You choose '{scheduler}' as scheduler. Download cookiecutter:\n    "
            f"https://github.com/Snakemake-Profiles/{scheduler.lower()}.git",
            fg="yellow")
        cookiecutter(f'https://github.com/Snakemake-Profiles/{scheduler.lower()}.git',
                     checkout=None,
                     no_input=True,
                     extra_context={"profile_name": f'',
                                    "sbatch_defaults": "--export=ALL",
                                    "cluster_config": f"$HOME/.config/{snake_installer.soft_name}/cluster_config.yaml",
                                    "advanced_argument_conversion": 1,
                                    "cluster_name": ""
                                    },
                     replay=False, overwrite_if_exists=True,
                     output_dir=f'{default_profile}', config_file=None,
                     default_config=False, password=None, directory=None, skip_if_file_exists=True)

        try:
            # default slurm cookiecutter not contain all snakemake variables
            if scheduler == "slurm":
                default_slurm = 'restart-times: 0\njobscript: "slurm-jobscript.sh"\ncluster: ' \
                                '"slurm-submit.py"\ncluster-status: "slurm-status.py"\nmax-jobs-per-second: ' \
                                '1\nmax-status-checks-per-second: 10\nlocal-cores: 1\njobs: 200\nlatency-wait: ' \
                                '1296000\n'
                extra_slurm = f"use-envmodules: {'true' if env == 'modules' else 'false'}\nuse-singularity: " \
                              f"{'true' if env == 'singularity' else 'false'}\nrerun-incomplete: " \
                              f"true\nprintshellcmds: true"
                with open(f"{default_profile}/config.yaml", "w") as config_file:
                    config_file.write(f"{default_slurm}{extra_slurm}")

                # adding a line in RESOURCES_MAPPING dico in slurm profile
                with open(f"{default_profile}/slurm-submit.py", "r") as slurm_submit_script:
                    search_text = '"nodes": ("nodes", "nnodes"),'
                    replace_text = '"nodes": ("nodes", "nnodes"),\n    "nodelist" : ("w", "nodelist"),'
                    data = slurm_submit_script.read()
                    data = data.replace(search_text, replace_text)
                with open(f"{default_profile}/slurm-submit.py", "w") as slurm_submit_script:
                    slurm_submit_script.write(data)

            click.secho(f"\n    Profile is success install on {default_profile}", fg="yellow")
        except Abort:
            snake_installer.fail()
    except Abort:
        click.secho(f"\n    Profile is already created, skipping {default_profile}", fg="yellow")
    except Exception as e:
        print(e)
        snake_installer.fail()
    try:
        # if singularity activation
        if env == 'singularity':
            # check if already download
            snake_installer.check_and_download_singularity()
            git_tools_file = snake_installer.git_tools_path.open("r").read()
            snake_installer.git_tools_path.open("w").write(git_tools_file.replace("{install_path}", f"{snake_installer.install_path}"))
        # export to add bash completion
        if bash_completion:
            snake_installer.create_bash_completion()
        click.secho(f"\n    Congratulations, you have successfully installed {snake_installer.soft_name} !!!\n\n", fg="green", bold=True)
        snake_installer.install_mode_file.open("w").write("cluster")
    except Exception as e:
        click.secho(f"\n    ERROR : an error was detected, please check {e}", fg="red")
        snake_installer.fail()


def __install_local(snake_installer, bash_completion):
    """Run installation for local computer downloading singularity images automatically."""
    # rm previous install (ie @julie cluster then local)
    snake_installer.clean_home()
    # add path to download
    snake_installer.install_path.joinpath("containers").mkdir(exist_ok=True, parents=True)
    try:
        snake_installer.check_and_download_singularity()
        # export to add bash completion
        if bash_completion:
            snake_installer.create_bash_completion()
        # Edit tools to write good path for snakefile
        git_tools_file = snake_installer.git_tools_path.open("r").read()
        snake_installer.user_tools_path.parent.mkdir(exist_ok=True, parents=True)
        snake_installer.user_tools_path.open("w").write(git_tools_file.replace("{install_path}", f"{snake_installer.install_path.as_posix()}"))
        # good install
        click.secho(f"\n    Congratulations, you have successfully installed {snake_installer.soft_name} !!!\n\n", fg="green", bold=True)
        snake_installer.install_mode_file.open("w").write("local")
    except Exception as e:
        snake_installer.install_mode_file.unlink(missing_ok=True)
        click.secho(f"\n    ERROR : an error was detected, please check {e}", fg="red")
        raise SystemExit


def __test_install(snake_installer, data_dir):
    """Test_install function downloads a scaled data test, writes a configuration file adapted to it and proposes a command line already to run !!!"""
    # create dir test and configure config.yaml
    data_dir = Path(data_dir).resolve()
    click.secho(f"\n    Created data test dir {data_dir}\n", fg="yellow")
    data_dir.mkdir(parents=True, exist_ok=True)

    data_config_path = data_dir.joinpath("data_test_config.yaml")
    click.secho(f"    Created config file to run data test: {data_config_path}\n", fg="yellow")
    txt = snake_installer.git_config_path.open("r").read().replace("DATA_DIR", f"{data_dir}").replace(
        f"./{snake_installer.soft_name}_OUTPUT/", f"{data_dir}/{snake_installer.soft_name}_OUTPUT/")
    data_config_path.open("w").write(txt)

    # download data
    download_zip = data_dir.joinpath(snake_installer.datatest_url_files[1])
    if not Path(download_zip.as_posix()[:-4]).exists():
        if not download_zip.exists():
            click.secho(f"    Download data test\n", fg="yellow")
            results = multiprocessing_download(
                [(snake_installer.datatest_url_files[0], download_zip.as_posix())], threads=1)
            for r in results:
                click.secho(r, fg="blue")
        click.secho(f"    Extract archive {download_zip} to {data_dir.as_posix()}\n", fg="yellow")
        unpack_archive(download_zip.as_posix(), data_dir.as_posix())
        download_zip.unlink()

    # build command line
    click.secho(f"    Write command line to run workflow on data test:\n", fg="yellow")
    mode = snake_installer.install_mode
    cmd = f"\n    {snake_installer.soft_name} {'run_cluster' if mode == 'cluster' else 'run_local --threads 1'} --config {data_config_path}\n\n"
    click.secho(cmd, fg='bright_blue')
