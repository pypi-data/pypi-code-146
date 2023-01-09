# import rich_click as click
import click
import sys
from .snake_wrapper import SnakeInstaller
from .usefull_function import __command_required_option_from_option, __replace_package_name, __add_header
from .global_variable import __dict_context_settings

from .install import __install_local, __install_cluster, __test_install, __required_options
from .edit_files import __edit_tools, __edit_cluster_config, __create_config
from .run import __run_cluster, __run_local


def main_wrapper(dico_tool=None, soft_path=None, url=None, docs=None, description_tool=None, singularity_url_files=None, datatest_url_files=None, **kargs) -> click.Group:
    """Use to wrapped snakemake workflow

        Args:
            dico_tool (``dict``): The dict structure provided of wrapped workflow
            or
            soft_path (str): The path of wrapped workflow installation
            url (str): Url of versioning repository (GitHub or GitLab)
            docs (str): Url of documentation
            description_tool (str):The header print on terminal when run programme. Please add string values 'VERSION', 'GIT_URL' and 'DOCS' and wrapper automatically replace by th good values
            singularity_url_files (list(tuple()): List of tuple with downloaded url and install destination with INSTALL_PATH. like INSTALL_PATH/containers/Singularity.CulebrONT_tools.sif
            datatest_url_files (tuple): Tuple with 2 values, first the url of datatest, second download name.
        Return:
            click.Group (``click.Group``): all sub-commands of workflow deployement and run

        Exemple:
            >>> from snakecdysis import main_wrapper
            >>> from podiumASM import dico_tool
            >>> main = main_wrapper(**dico_tool)
            >>> main()
            >>> main = main_wrapper(soft_path="path/to/install", url="http://Snakecdysis.com", docs=docs, description_tool=description_tool,  singularity_ur_files=singularity_url_files, datatest_url_files=datatest_url_files)
    """

    if dico_tool:
        snake_installer = SnakeInstaller(**dico_tool)
    else:
        snake_installer = SnakeInstaller(soft_path=soft_path, url=url, docs=docs, description_tool=description_tool, singularity_ur_files=singularity_ur_files, datatest_url_files=datatest_url_files, **kargs)

    # Create click group for all subcommand line
    @click.group(name=f"{snake_installer.soft_name}", context_settings=__dict_context_settings,
                 invoke_without_command=True, no_args_is_help=True)
    @click.option('--restore', '-r', is_flag=True, required=False, default=False, show_default=True,
                  help='Restore installation mode (need root or sudo)')
    @click.version_option(snake_installer.version, "-v", "--version", message="%(prog)s, version %(version)s")
    @click.pass_context
    @__add_header(snake_installer=snake_installer)
    def main_command(ctx, restore):
        """"""
        if ctx.invoked_subcommand is None and restore:  # and check_privileges():
            if snake_installer.install_mode in ["local", "cluster"]:
                snake_installer.install_mode_file.unlink(missing_ok=False)
                snake_installer.clean_home()
                click.secho(
                    f"\n    Remove installation mode, now run:\n    {snake_installer.soft_name} install_local or "
                    f"install_cluster\n\n", fg="yellow")
            else:
                click.secho(
                    f"\n    No reset need, {snake_installer.soft_name} not install !!!!!\n    Please run: "
                    f"{snake_installer.soft_name} install_local or install_cluster !!!!\n\n",
                    fg="red")

    ############################################
    # Install mode subcommand
    ############################################
    # LOCAL
    @click.command("install_local", short_help=f'Install {snake_installer.soft_name} on local computer',
                   context_settings=dict(max_content_width=800), no_args_is_help=False)
    @click.option('--bash_completion/--no-bash_completion', is_flag=True, required=False, default=True,
                  show_default=True,
                  help=f'Allow bash completion of {snake_installer.soft_name} commands on the bashrc file')
    @__replace_package_name(snake_installer=snake_installer)
    def install_local(bash_completion):
        """Run installation for local computer downloading singularity images automatically."""
        __install_local(snake_installer, bash_completion)

    # CLUSTER
    @click.command("install_cluster", short_help=f'Install {snake_installer.soft_name} on HPC cluster',
                   context_settings=__dict_context_settings,
                   cls=__command_required_option_from_option('create_envmodule', __required_options),
                   no_args_is_help=True)
    @click.option('--scheduler', '-s', default="slurm", type=click.Choice(['slurm'], case_sensitive=False),
                  prompt='Choose your HPC scheduler', show_default=True,
                  help='Type the HPC scheduler (for the moment, only slurm is available ! )')
    @click.option('--env', '-e', default="modules", type=click.Choice(['modules', 'singularity'], case_sensitive=False),
                  prompt='Choose mode for tools dependencies', show_default=True, help='Mode for tools dependencies ')
    @click.option('--bash_completion/--no-bash_completion', is_flag=True, required=False, default=True,
                  show_default=True,
                  help=f'Allow bash completion of {snake_installer.soft_name} commands on the bashrc file')
    def install_cluster(scheduler, env, bash_completion):
        """Run installation of tool for HPC cluster"""
        __install_cluster(snake_installer, scheduler, env, bash_completion)

    # TEST INSTALL
    @click.command("test_install",
                   short_help=f'Test {snake_installer.soft_name} with data_test after install (local or cluster)',
                   context_settings=__dict_context_settings, no_args_is_help=False)
    @click.option('--data_dir', '-d', default=None,
                  type=click.Path(exists=False, file_okay=False, dir_okay=True, readable=True, resolve_path=True),
                  required=True, show_default=False,
                  help='Path to download data test and create config.yaml to run test')
    @__replace_package_name(snake_installer=snake_installer)
    def test_install(data_dir):
        """Test_install function downloads a scaled data test, writes a configuration file adapted to it and
        proposes a command line already to run !!!"""
        __test_install(snake_installer, data_dir)

    ############################################
    # Run mode subcommand
    ############################################

    @click.command("run_local", short_help='Run a workflow on local computer (use singularity mandatory)',
                   context_settings=__dict_context_settings, no_args_is_help=True)
    @click.option('--config', '-c', type=click.Path(exists=True, file_okay=True, readable=True, resolve_path=True),
                  required=True, help=f'Configuration file for run tool')
    @click.option('--threads', '-t', type=int, required=True, help='Number of threads')
    @click.option('--pdf', '-p', is_flag=True, required=False, default=False,
                  help='Run snakemake with --dag, --rulegraph and --filegraph')
    @click.argument('snakemake_other', nargs=-1, type=click.UNPROCESSED)
    @__replace_package_name(snake_installer=snake_installer)
    def run_local(config, threads, pdf, snakemake_other):
        """
        \b
        Run snakemake command line with mandatory parameters.
        SNAKEMAKE_OTHER: You can also pass additional Snakemake parameters using snakemake syntax.
        These parameters will take precedence over Snakemake ones, which were defined in the profile.
        See: https://snakemake.readthedocs.io/en/stable/executing/cli.html
        \b
        Example:
            tool run_local -c config.yaml --threads 8 --dry-run
            tool run_local -c config.yaml --threads 8 --singularity-args '--bind /mnt:/mnt'
        """
        __run_local(snake_installer, config, threads, pdf, snakemake_other)
        pass

    @click.command("run_cluster", short_help='Run workflow on HPC',
                   context_settings=__dict_context_settings, no_args_is_help=True)
    @click.option('--config', '-c', type=click.Path(exists=True, file_okay=True, readable=True, resolve_path=True),
                  required=True, show_default=True, help=f'Configuration file for run tool')
    @click.option('--pdf', '-pdf', is_flag=True, required=False, default=False, show_default=True,
                  help='Run snakemake with --dag, --rulegraph and --filegraph')
    @click.argument('snakemake_other', nargs=-1, type=click.UNPROCESSED)
    @__replace_package_name(snake_installer=snake_installer)
    def run_cluster(config, pdf, snakemake_other):
        """
        \b
        Run snakemake command line with mandatory parameters.
        SNAKEMAKE_OTHER: You can also pass additional Snakemake parameters using snakemake syntax.
        These parameters will take precedence over Snakemake ones, which were defined in the profile.
        See: https://snakemake.readthedocs.io/en/stable/executing/cli.html
        \b
        Example:
            tool run_cluster -c config.yaml --dry-run --jobs 200
        """
        __run_cluster(snake_installer, config, pdf, snakemake_other)

    ############################################
    # EDIT CONFIG subcommand
    ############################################

    @click.command("edit_tools", short_help='Edit own tools version', no_args_is_help=False)
    @click.option('--restore', '-r', is_flag=True, required=False, default=False, show_default=True,
                  help='Restore default tools_config.yaml (from install)')
    @__replace_package_name(snake_installer=snake_installer)
    def edit_tools(restore):
        """"""
        __edit_tools(snake_installer, restore)

    @click.command("create_config", short_help='Create config.yaml for run', no_args_is_help=True)
    @click.option('--configyaml', '-c', default=None,
                  type=click.Path(exists=False, file_okay=True, dir_okay=False, readable=True, resolve_path=True),
                  required=True, show_default=True, help='Path to create config.yaml')
    @__replace_package_name(snake_installer=snake_installer)
    def create_config(configyaml):
        """"""
        __create_config(snake_installer, configyaml)

    @click.command("edit_cluster_config", short_help='Edit cluster_config.yaml use by profile', no_args_is_help=False)
    @__replace_package_name(snake_installer=snake_installer)
    def edit_cluster_config():
        """"""
        __edit_cluster_config(snake_installer)

    # Hack for build docs with unspecified install
    args = str(sys.argv)
    if "sphinx" in args:
        main_command.add_command(run_cluster)
        main_command.add_command(edit_cluster_config)
        main_command.add_command(create_config)
        main_command.add_command(edit_tools)
        main_command.add_command(run_local)
        main_command.add_command(install_cluster)
        main_command.add_command(install_local)
        main_command.add_command(test_install)
    else:
        if snake_installer.install_mode == "cluster":
            main_command.add_command(test_install)
            main_command.add_command(run_cluster)
            main_command.add_command(edit_cluster_config)
            main_command.add_command(create_config)
            main_command.add_command(edit_tools)
        elif snake_installer.install_mode == "local":
            main_command.add_command(test_install)
            main_command.add_command(run_local)
            main_command.add_command(create_config)
        else:
            main_command.add_command(install_cluster)
            main_command.add_command(install_local)
    return main_command
