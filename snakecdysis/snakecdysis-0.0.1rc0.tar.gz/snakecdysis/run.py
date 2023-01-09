import click
from shutil import copyfile
import re
import subprocess
import sys


def rewrite_if_bind(snakemake_other):
    """
    Function to rewrite --bind params
    It modifies click.UNPROCESSED
    """
    bind_args = list(filter(re.compile(".*--bind.*").match, snakemake_other))  # Try to select --bind
    if bind_args:
        bind_args_rewrite = f'"--bind {bind_args[0].split(" ")[1]}"'
        snakemake_other_list = list(filter(lambda x: x not in bind_args[0], snakemake_other))  # remove value to rewrite
        snakemake_other_list.append(bind_args_rewrite)
        return snakemake_other_list
    else:
        return snakemake_other


def build_pdf(cmd_snakemake_base):
    dag_cmd_snakemake = f"{cmd_snakemake_base} --dag | dot -Tpdf > schema_pipeline_dag.pdf"
    click.secho(f"    {dag_cmd_snakemake}\n", fg='bright_blue')
    process = subprocess.run(dag_cmd_snakemake, shell=True, check=False, stdout=sys.stdout, stderr=sys.stderr)
    if int(process.returncode) >= 1:
        raise SystemExit
    rulegraph_cmd_snakemake = f"{cmd_snakemake_base} --rulegraph | dot -Tpdf > schema_pipeline_global.pdf"
    click.secho(f"    {rulegraph_cmd_snakemake}\n", fg='bright_blue')
    process = subprocess.run(rulegraph_cmd_snakemake, shell=True, check=False, stdout=sys.stdout, stderr=sys.stderr)
    if int(process.returncode) >= 1:
        raise SystemExit
    filegraph_cmd_snakemake = f"{cmd_snakemake_base} --filegraph | dot -Tpdf > schema_pipeline_files.pdf"
    click.secho(f"    {filegraph_cmd_snakemake}\n", fg='bright_blue')
    process = subprocess.run(filegraph_cmd_snakemake, shell=True, check=False, stdout=sys.stdout, stderr=sys.stderr)
    if int(process.returncode) >= 1:
        raise SystemExit


def __run_cluster(snake_installer, config, pdf, snakemake_other):
    """
    \b
    Run snakemake command line with mandatory parameters.
    SNAKEMAKE_OTHER: You can also pass additional Snakemake parameters
    using snakemake syntax.
    These parameters will take precedence over Snakemake ones, which were
    defined in the profile.
    See: https://snakemake.readthedocs.io/en/stable/executing/cli.html

    Example:
        rattleSNP run_cluster -c config.yaml --dry-run --jobs 200
    """
    profile = snake_installer.default_profile
    tools = snake_installer.git_tools_path
    clusterconfig = None
    # get user arguments
    click.secho(f'    Profile file: {profile}', fg='yellow')
    click.secho(f'    Config file: {config}', fg='yellow')

    if snake_installer.user_cluster_config.exists():
        clusterconfig = snake_installer.user_cluster_config
    else:
        click.secho(f"    Please run command line '{snake_installer.soft_name} edit_cluster_config' before the first run of {snake_installer.soft_name} see {snake_installer.docs}", fg="red", err=True)
        exit()
    cmd_clusterconfig = f"--cluster-config {clusterconfig}"
    click.secho(f'    Cluster config file load: {clusterconfig}', fg='yellow')

    if tools != snake_installer.git_tools_path.as_posix():
        snake_installer.args_tools_path.parent.mkdir(parents=True, exist_ok=True)
        copyfile(tools, snake_installer.args_tools_path)
    elif snake_installer.user_tools_path.exists():
        tools = snake_installer.user_tools_path
    click.secho(f'    Tools Path file: {tools}', fg='yellow')

    cmd_snakemake_base = f"snakemake --show-failed-logs -p -s {snake_installer.snakefile} --configfile {config} --profile {profile} {cmd_clusterconfig} {' '.join(rewrite_if_bind(snakemake_other))}"
    click.secho(f"\n    {cmd_snakemake_base}\n", fg='bright_blue')
    process = subprocess.run(cmd_snakemake_base, shell=True, check=False, stdout=sys.stdout, stderr=sys.stderr)
    if int(process.returncode) >= 1:
        raise SystemExit

    if pdf:
        build_pdf(cmd_snakemake_base)


def __run_local(snake_installer, config, threads, pdf, snakemake_other):
    """
    \b
    Run snakemake command line with mandatory parameters.
    SNAKEMAKE_OTHER: You can also pass additional Snakemake parameters
    using snakemake syntax.
    These parameters will take precedence over Snakemake ones, which were
    defined in the profile.
    See: https://snakemake.readthedocs.io/en/stable/executing/cli.html

    Example:

        rattleSNP run_local -c config.yaml --threads 8 --dry-run

        rattleSNP run_local -c config.yaml --threads 8 --singularity-args '--bind /mnt:/mnt'

        # in LOCAL using 6 threads for Canu assembly from the total 8 threads\n
        rattleSNP run_local -c config.yaml --threads 8 --set-threads run_canu=6

    """
    click.secho(f'    Config file: {config}', fg='yellow')
    click.secho(f'    Tools config file: {snake_installer.user_tools_path}', fg='yellow')

    cmd_snakemake_base = f"snakemake --latency-wait 1296000 --cores {threads} --use-singularity --show-failed-logs --printshellcmds -s {snake_installer.snakefile} --configfile {config}  {' '.join(rewrite_if_bind(snakemake_other))}"
    click.secho(f"\n    {cmd_snakemake_base}\n", fg='bright_blue')
    process = subprocess.run(cmd_snakemake_base, shell=True, check=False, stdout=sys.stdout, stderr=sys.stderr)
    if int(process.returncode) >= 1:
        raise SystemExit

    if pdf:
        build_pdf(cmd_snakemake_base)
