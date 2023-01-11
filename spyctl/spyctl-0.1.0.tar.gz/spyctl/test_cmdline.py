import click
import inspect
from typing import Dict, List

MAIN_EPILOG = (
    'Use "spyctl <command> --help" for more information about a given command'
)


class CustomGroup(click.Group):
    SECTION_BASIC = "Basic Commands"
    SECTION_OTHER = "Other Commands"
    command_sections = [SECTION_BASIC, SECTION_OTHER]
    cmd_to_section_map = {
        "apply": SECTION_BASIC,
        "create": SECTION_BASIC,
        "delete": SECTION_BASIC,
        "diff": SECTION_BASIC,
        "get": SECTION_BASIC,
        "merge": SECTION_BASIC,
    }

    def format_help(
        self, ctx: click.Context, formatter: click.HelpFormatter
    ) -> None:
        self.format_help_text(ctx, formatter)
        self.format_options(ctx, formatter)
        self.format_usage(ctx, formatter)
        self.format_epilog(ctx, formatter)

    def format_help_text(
        self, ctx: click.Context, formatter: click.HelpFormatter
    ) -> None:
        text = self.help if self.help is not None else ""

        if text:
            text = inspect.cleandoc(text).partition("\f")[0]
            formatter.write_paragraph()
            formatter.write_text(text)

    def format_usage(
        self, ctx: click.Context, formatter: click.HelpFormatter
    ) -> None:
        formatter.write_paragraph()
        formatter.write_text("Usage:")
        formatter.indent()
        formatter.write_text("spyctl [flags] [options]")
        formatter.dedent()

    def format_epilog(
        self, ctx: click.Context, formatter: click.HelpFormatter
    ) -> None:
        """Writes the epilog into the formatter if it exists."""
        if self.epilog:
            epilog = inspect.cleandoc(self.epilog)
            formatter.write_paragraph()
            formatter.write_text(epilog)

    def format_commands(
        self, ctx: click.Context, formatter: click.HelpFormatter
    ) -> None:
        commands = []
        for subcommand in self.list_commands(ctx):
            cmd = self.get_command(ctx, subcommand)
            # What is this, the tool lied about a command.  Ignore it
            if cmd is None:
                continue
            if cmd.hidden:
                continue

            commands.append((subcommand, cmd))

        # allow for 3 times the default spacing
        if len(commands):
            limit = formatter.width - 6 - max(len(cmd[0]) for cmd in commands)

            sections: Dict[str, List] = {}
            for section_title in self.command_sections:
                sections.setdefault(section_title, [])
            for subcommand, cmd in commands:
                section_title = self.cmd_to_section_map.get(subcommand)
                if not section_title:
                    section_title = self.SECTION_OTHER
                help = cmd.get_short_help_str(limit)
                sections[section_title].append((subcommand, help))

            for title, rows in sections.items():
                if rows:
                    with formatter.section(title):
                        formatter.write_dl(rows, col_spacing=4)


class CustomSubGroup(click.Group):
    def group(self, *args, **kwargs):
        """Behaves the same as `click.Group.group()` except if passed
        a list of names, all after the first will be aliases for the first.
        """

        def decorator(f):
            aliased_group = []
            if isinstance(args[0], list):
                # we have a list so create group aliases
                _args = [args[0][0]] + list(args[1:])
                for alias in args[0][1:]:
                    grp = super(CustomGroup, self).group(
                        alias, *args[1:], **kwargs
                    )(f)
                    grp.short_help = "Alias for '{}'".format(_args[0])
                    aliased_group.append(grp)
            else:
                _args = args

            # create the main group
            grp = super(CustomGroup, self).group(*_args, **kwargs)(f)

            # for all of the aliased groups, share the main group commands
            for aliased in aliased_group:
                aliased.commands = grp.commands

            return grp

        return decorator

    def format_help(
        self, ctx: click.Context, formatter: click.HelpFormatter
    ) -> None:
        self.format_help_text(ctx, formatter)
        self.format_options(ctx, formatter)
        self.format_usage(ctx, formatter)
        self.format_epilog(ctx, formatter)

    def format_help_text(
        self, ctx: click.Context, formatter: click.HelpFormatter
    ) -> None:
        text = self.help if self.help is not None else ""

        if text:
            text = inspect.cleandoc(text).partition("\f")[0]
            formatter.write_paragraph()
            formatter.write_text(text)

    def format_usage(
        self, ctx: click.Context, formatter: click.HelpFormatter
    ) -> None:
        formatter.write_paragraph()
        prefix = "Usage:\n  "
        pieces = self.collect_usage_pieces(ctx)
        formatter.write_usage(
            ctx.command_path, " ".join(pieces), prefix=prefix
        )
        formatter.dedent()

    def format_epilog(
        self, ctx: click.Context, formatter: click.HelpFormatter
    ) -> None:
        """Writes the epilog into the formatter if it exists."""
        if self.epilog:
            epilog = inspect.cleandoc(self.epilog)
            formatter.write_paragraph()
            formatter.write_text(epilog)

    def format_commands(
        self, ctx: click.Context, formatter: click.HelpFormatter
    ) -> None:
        commands = []
        for subcommand in self.list_commands(ctx):
            cmd = self.get_command(ctx, subcommand)
            # What is this, the tool lied about a command.  Ignore it
            if cmd is None:
                continue
            if cmd.hidden:
                continue

            commands.append((subcommand, cmd))

        # allow for 3 times the default spacing
        if len(commands):
            limit = formatter.width - 6 - max(len(cmd[0]) for cmd in commands)

            rows = []
            for subcommand, cmd in commands:
                help = cmd.get_short_help_str(limit)
                rows.append((subcommand, help))

            if rows:
                with formatter.section("Available Commands"):
                    formatter.write_dl(rows, col_spacing=4)


class CustomCommand(click.Command):
    def format_help(
        self, ctx: click.Context, formatter: click.HelpFormatter
    ) -> None:
        self.format_help_text(ctx, formatter)
        self.format_options(ctx, formatter)
        self.format_usage(ctx, formatter)
        self.format_epilog(ctx, formatter)

    def format_help_text(
        self, ctx: click.Context, formatter: click.HelpFormatter
    ) -> None:
        text = self.help if self.help is not None else ""

        if text:
            text = inspect.cleandoc(text).partition("\f")[0]
            formatter.write_paragraph()
            formatter.write_text(text)

    def format_usage(
        self, ctx: click.Context, formatter: click.HelpFormatter
    ) -> None:
        formatter.write_paragraph()
        prefix = "Usage:\n  "
        pieces = self.collect_usage_pieces(ctx)
        formatter.write_usage(
            ctx.command_path, " ".join(pieces), prefix=prefix
        )
        formatter.dedent()

    def format_epilog(
        self, ctx: click.Context, formatter: click.HelpFormatter
    ) -> None:
        """Writes the epilog into the formatter if it exists."""
        if self.epilog:
            epilog = inspect.cleandoc(self.epilog)
            formatter.write_paragraph()
            formatter.write_text(epilog)


# ----------------------------------------------------------------- #
#                     Command Tree Entrypoint                       #
# ----------------------------------------------------------------- #


@click.group(cls=CustomGroup, epilog=MAIN_EPILOG)
@click.help_option("-h", "--help", hidden=True)
def main():
    """spyctl displays and controls objects within your Spyderbat
    environment
    """
    pass


# ----------------------------------------------------------------- #
#                         Apply Subcommand                          #
# ----------------------------------------------------------------- #


@main.command("apply", cls=CustomCommand, epilog=MAIN_EPILOG)
@click.help_option("-h", "--help", hidden=True)
@click.option("-f", "--filename")
def apply(filename):
    """Apply a configuration to a resource by file name."""
    click.echo(filename)


# ----------------------------------------------------------------- #
#                        Delete Subcommand                          #
# ----------------------------------------------------------------- #


@main.command("delete", cls=CustomCommand, epilog=MAIN_EPILOG)
@click.help_option("-h", "--help", hidden=True)
@click.argument("resource")
@click.argument("name_or_id")
def delete(resource, name_or_id):
    """Delete resources by resource and names, or by resource and ids"""
    pass


# ----------------------------------------------------------------- #
#                          Diff Subcommand                          #
# ----------------------------------------------------------------- #


@main.command("diff", cls=CustomCommand, epilog=MAIN_EPILOG)
@click.help_option("-h", "--help", hidden=True)
@click.option(
    "-f",
    "--filename",
    help="Target file of the diff.",
    metavar="",
)
@click.option(
    "-w",
    "--with-file",
    help="File to diff with target file.",
    metavar="",
)
@click.option(
    "-l",
    "--latest",
    help="Diff file with latest records using the value of lastTimestamp in"
    " metadata",
    metavar="",
)
def diff(filename, with_file=None, latest=None):
    """Diff FingerprintsGroups with SpyderbatBaselines and SpyderbatPolicies"""
    pass


# ----------------------------------------------------------------- #
#                         Config Subcommand                         #
# ----------------------------------------------------------------- #


@main.group("config", cls=CustomSubGroup, epilog=MAIN_EPILOG)
@click.help_option("-h", "--help", hidden=True)
def config():
    """Modify spyctl config files."""
    pass


@config.command("delete-context", cls=CustomCommand, epilog=MAIN_EPILOG)
@click.help_option("-h", "--help", hidden=True)
@click.option(
    "-g",
    "--global",
    "force_global",
    type=bool,
    help="When operating within a spyctl workspace, this forces a change to"
    " the global spyctl config.",
)
def delete_context(force_global=False):
    """Delete the specified context from a spyctl configuration file."""
    pass


@config.command("current-context", cls=CustomCommand, epilog=MAIN_EPILOG)
@click.help_option("-h", "--help", hidden=True)
@click.option(
    "-g",
    "--global",
    "force_global",
    type=bool,
    help="When operating within a spyctl workspace, this forces a change to"
    " the global spyctl config.",
)
def current_context():
    """Display the current-context."""
    pass


@config.command("set-context", cls=CustomCommand, epilog=MAIN_EPILOG)
@click.help_option("-h", "--help", hidden=True)
@click.option(
    "-g",
    "--global",
    "force_global",
    type=bool,
    help="When operating within a spyctl workspace, this forces a change to"
    " the global spyctl config.",
)
def set_context():
    """Set a context entry in a spyctl configuration file."""
    pass


@config.command("use-context", cls=CustomCommand, epilog=MAIN_EPILOG)
@click.help_option("-h", "--help", hidden=True)
@click.option(
    "-g",
    "--global",
    "force_global",
    type=bool,
    help="When operating within a spyctl workspace, this forces a change to"
    " the global spyctl config.",
)
def use_context():
    """Set the current-context in a spyctl configuration file."""
    pass


@config.command("view", cls=CustomCommand, epilog=MAIN_EPILOG)
@click.help_option("-h", "--help", hidden=True)
@click.option(
    "-w",
    "--workspace",
    "force_workspace",
    type=bool,
    help="Default behavior is to show the combined config between global and"
    " workspace including all available contexts. This forces spyctl to only"
    " show the contents of the workspace config file.",
)
def view():
    """View the current spyctl configuration file(s)."""
    pass


# ----------------------------------------------------------------- #
#                         Create Subcommand                         #
# ----------------------------------------------------------------- #


@main.group("create", cls=CustomSubGroup, epilog=MAIN_EPILOG)
@click.help_option("-h", "--help", hidden=True)
def create():
    """Create a resource from a file."""
    pass


@create.command("baseline", cls=CustomCommand, epilog=MAIN_EPILOG)
@click.help_option("-h", "--help", hidden=True)
@click.option(
    "-f",
    "--from-file",
    "filename",
    help="File that contains the FingerprintsGroup object, from which spyctl"
    " creates a baseline.",
    metavar="",
)
def create_baseline(filename):
    """Create a SpyderbatBaseline from a file, outputted to stdout"""
    click.echo(filename)


@create.command("policy", cls=CustomCommand, epilog=MAIN_EPILOG)
@click.help_option("-h", "--help", hidden=True)
@click.option(
    "-f",
    "--from-file",
    "filename",
    help="File that contains the FingerprintsGroup or SpyderbatBaseline"
    " object, from which spyctl creates a policy",
    metavar="",
)
def create_policy(filename):
    """Create a SpyderbatPolicy object from a file, outputted to stdout"""
    click.echo(filename)


# ----------------------------------------------------------------- #
#                          Get Subcommand                           #
# ----------------------------------------------------------------- #


@main.group("get", cls=CustomSubGroup, epilog=MAIN_EPILOG)
@click.help_option("-h", "--help", hidden=True)
def get():
    """Display one or many resources."""
    pass


@get.command("clusters", cls=CustomCommand, epilog=MAIN_EPILOG)
@click.help_option("-h", "--help", hidden=True)
@click.option(
    "--image",
    help="Only show clusters with pods or nodes running this container image."
    " Overrides current context.",
)
@click.option(
    "--image-id",
    help="Only show clusters with pods or nodes running containers with this"
    " image id. Overrides current context.",
)
@click.option(
    "--container-name",
    help="Only show clusters with pods or node running containers with this"
    " container name. Overrides current context.",
)
@click.option(
    "--cgroup",
    help="Only show clusters with nodes running Linux services with this"
    " cgroup. Overrides current context.",
)
@click.option(
    "--pods",
    help="Only show clusters with nodes running these pods. Overrides current"
    " context",
)
@click.option(
    "--machines",
    "--nodes",
    help="Only show clusters linked to these nodes. Overrides current"
    " context.",
)
@click.option(
    "-t" "--start-time",
    help="Start time of the query. Default is beginning of time.",
)
@click.option("-e" "--end-time", help="End time of the query. Default is now.")
def get_clusters():
    """Display one or many clusters."""
    pass


@get.command("container-images", cls=CustomCommand, epilog=MAIN_EPILOG)
@click.help_option("-h", "--help", hidden=True)
@click.option(
    "--image",
    help="Only show container images matching this image criteria. Overrides"
    " current context.",
)
@click.option(
    "--image-id",
    help="Only show container images matching this id criteria."
    " Overrides current context.",
)
@click.option(
    "--container-name",
    help="Only show container images matching this container name criteria"
    " this container name criteria. Overrides current context.",
)
@click.option(
    "--pods",
    help="Only show container images for containers running in these pods."
    " Overrides current context",
)
@click.option(
    "-l",
    "--pod-selectors",
    help="Pod selector (label query) to filter on, supports '=', '==', and"
    " '!='.(e.g. -l key1=value1,key2=value2). Matching"
    "objects must satisfy all of the specified label constraints.",
)
@click.option(
    "-n",
    "--namespace-selectors",
    help="Namespace selector (label query) to filter on, supports '=', '==',"
    " and '!='.(e.g. -l key1=value1,key2=value2). Matching"
    "objects must satisfy all of the specified label constraints.",
)
@click.option(
    "--machines",
    "--nodes",
    help="Only show container images for containers linked to these nodes."
    " Overrides current context.",
)
@click.option(
    "--clusters",
    help="Only show container images for containers within these clusters."
    " Overrides current context",
)
@click.option(
    "-t" "--start-time",
    help="Start time of the query. Default is beginning of time.",
)
@click.option("-e" "--end-time", help="End time of the query. Default is now.")
def get_container_images():
    """Display one or many container images. Displays image and image ID"""
    pass


@get.command("container-names", cls=CustomCommand, epilog=MAIN_EPILOG)
@click.help_option("-h", "--help", hidden=True)
@click.option(
    "--image",
    help="Only show container-names with this container image. Overrides"
    " current context.",
)
@click.option(
    "--image-id",
    help="Only show container names with with"
    " this image id. Overrides current context.",
)
@click.option(
    "--container-name",
    help="Only show container names matching"
    " this container name criteria. Overrides current context.",
)
@click.option(
    "--pods",
    help="Only show container names for containers running in these pods."
    " Overrides current context",
)
@click.option(
    "-l",
    "--pod-selectors",
    help="Pod selector (label query) to filter on, supports '=', '==', and"
    " '!='.(e.g. -l key1=value1,key2=value2). Matching"
    "objects must satisfy all of the specified label constraints.",
)
@click.option(
    "-n",
    "--namespace-selectors",
    help="Namespace selector (label query) to filter on, supports '=', '==',"
    " and '!='.(e.g. -l key1=value1,key2=value2). Matching"
    "objects must satisfy all of the specified label constraints.",
)
@click.option(
    "--machines",
    "--nodes",
    help="Only show container names for containers linked to these nodes."
    " Overrides current context.",
)
@click.option(
    "--clusters",
    help="Only show container names for containers within these clusters."
    " Overrides current context",
)
@click.option(
    "-t" "--start-time",
    help="Start time of the query. Default is beginning of time.",
)
@click.option("-e" "--end-time", help="End time of the query. Default is now.")
def get_images():
    """Display one or many names of containers running in your"
    " environment.
    """
    pass


@get.command("fingerprints", cls=CustomCommand, epilog=MAIN_EPILOG)
@click.help_option("-h", "--help", hidden=True)
@click.option(
    "--image",
    help="Only show fingerprints with this container image. Overrides current"
    " context.",
)
@click.option(
    "--image-id",
    help="Only show fingerprints with with"
    " this image id. Overrides current context.",
)
@click.option(
    "--container-name",
    help="Only show fingerprints with"
    " this container name. Overrides current context.",
)
@click.option(
    "--cgroup",
    help="Only show fingerprints of Linux services with this"
    " cgroup. Overrides current context.",
)
@click.option(
    "--pods",
    help="Only show fingerprints with nodes running these pods. Overrides"
    " current context",
)
@click.option(
    "-l",
    "--pod-selectors",
    help="Pod selector (label query) to filter on, supports '=', '==', and"
    " '!='.(e.g. -l key1=value1,key2=value2). Matching"
    "objects must satisfy all of the specified label constraints.",
)
@click.option(
    "-n",
    "--namespace-selectors",
    help="Namespace selector (label query) to filter on, supports '=', '==',"
    " and '!='.(e.g. -l key1=value1,key2=value2). Matching"
    "objects must satisfy all of the specified label constraints.",
)
@click.option(
    "--machines",
    "--nodes",
    help="Only show fingerprints linked to these nodes. Overrides current"
    " context.",
)
@click.option(
    "--clusters",
    help="Only show fingerprints within these clusters. Overrides current"
    " context",
)
@click.option(
    "-t" "--start-time",
    help="Start time of the query. Default is beginning of time.",
)
@click.option("-e" "--end-time", help="End time of the query. Default is now.")
def get_fingerprints():
    """Display one or many fingerprints."""
    pass


@get.command("linux-services", cls=CustomCommand, epilog=MAIN_EPILOG)
@click.help_option("-h", "--help", hidden=True)
@click.option(
    "--cgroup",
    help="Only show linux-services with nodes running Linux services with this"
    " name. Overrides current context.",
)
@click.option(
    "--machines",
    "--nodes",
    help="Only show linux-services on these machines. Overrides current"
    " context.",
)
@click.option(
    "--clusters",
    help="Only show linux-services within these clusters. Overrides current"
    " context",
)
@click.option(
    "-t" "--start-time",
    help="Start time of the query. Default is beginning of time.",
)
@click.option("-e" "--end-time", help="End time of the query. Default is now.")
@click.option(
    "-t" "--start-time",
    help="Start time of the query. Default is beginning of time.",
)
@click.option("-e" "--end-time", help="End time of the query. Default is now.")
def get_linux_services():
    """Display one or many linux services."""
    pass


@get.command("machines", cls=CustomCommand, epilog=MAIN_EPILOG)
@click.help_option("-h", "--help", hidden=True)
@click.option(
    "--image",
    help="Only show machines with pods or nodes running this container"
    " image. Overrides current context.",
)
@click.option(
    "--image-id",
    help="Only show machines with pods or nodes running containers with"
    " this image id. Overrides current context.",
)
@click.option(
    "--container-name",
    help="Only show machines with pods or node running containers with"
    " this name. Overrides current context.",
)
@click.option(
    "--cgroup",
    help="Only show machines with nodes running Linux services with this"
    " name. Overrides current context.",
)
@click.option(
    "--pods",
    help="Only show machines with nodes running these pods. Overrides"
    " current context",
)
@click.option(
    "--machines",
    "--nodes",
    help="Only show machines matching this criteria. Overrides current"
    " context.",
)
@click.option(
    "--clusters",
    help="Only show machines within these clusters. Overrides current"
    " context",
)
@click.option(
    "-t" "--start-time",
    help="Start time of the query. Default is beginning of time.",
)
@click.option("-e" "--end-time", help="End time of the query. Default is now.")
def get_machines():
    """Display one or many machines."""
    pass


@get.command("machine-groups", cls=CustomCommand, epilog=MAIN_EPILOG)
@click.help_option("-h", "--help", hidden=True)
def get_machines_groups():
    """Display one or many machine-groups."""
    pass


@get.command("pods", cls=CustomCommand, epilog=MAIN_EPILOG)
@click.help_option("-h", "--help", hidden=True)
@click.option(
    "--image",
    help="Only show pods running this container"
    " image. Overrides current context.",
)
@click.option(
    "--image-id",
    help="Only show pods running containers with"
    " this image id. Overrides current context.",
)
@click.option(
    "--container-name",
    help="Only show pods running containers with"
    " this name. Overrides current context.",
)
@click.option(
    "--pods",
    help="Only show pods matching this criteria. Overrides current context",
)
@click.option(
    "-l",
    "--pod-selectors",
    help="Pod selector (label query) to filter on, supports '=', '==', and"
    " '!='.(e.g. -l key1=value1,key2=value2). Matching"
    "objects must satisfy all of the specified label constraints.",
)
@click.option(
    "-n",
    "--namespace-selectors",
    help="Namespace selector (label query) to filter on, supports '=', '==',"
    " and '!='.(e.g. -l key1=value1,key2=value2). Matching"
    "objects must satisfy all of the specified label constraints.",
)
@click.option(
    "--machines",
    "--nodes",
    help="Only show pods running on these nodes. Overrides current"
    " context.",
)
@click.option(
    "--clusters",
    help="Only show pods within these clusters. Overrides current context",
)
@click.option(
    "-t" "--start-time",
    help="Start time of the query. Default is beginning of time.",
)
@click.option("-e" "--end-time", help="End time of the query. Default is now.")
def get_pods():
    """Display one or many pods."""
    pass


@get.command("policies", cls=CustomCommand, epilog=MAIN_EPILOG)
@click.help_option("-h", "--help", hidden=True)
@click.option(
    "--image",
    help="Only show machines with pods or nodes running this container"
    " image. Overrides current context.",
)
@click.option(
    "--image-id",
    help="Only show machines with pods or nodes running containers with"
    " this image id. Overrides current context.",
)
@click.option(
    "--container-name",
    help="Only show machines with pods or node running containers with"
    " this name. Overrides current context.",
)
@click.option(
    "--cgroup",
    help="Only show machines with nodes running Linux services with this"
    " name. Overrides current context.",
)
@click.option(
    "-l",
    "--pod-selectors",
    help="Pod selector (label query) to filter on, supports '=', '==', and"
    " '!='.(e.g. -l key1=value1,key2=value2). Matching"
    "objects must satisfy all of the specified label constraints.",
)
@click.option(
    "-n",
    "--namespace-selectors",
    help="Namespace selector (label query) to filter on, supports '=', '==',"
    " and '!='.(e.g. -l key1=value1,key2=value2). Matching"
    "objects must satisfy all of the specified label constraints.",
)
def get_policies():
    """Display one or many policies."""
    pass


@get.command("secrets", cls=CustomCommand, epilog=MAIN_EPILOG)
@click.help_option("-h", "--help", hidden=True)
def get_secrets():
    """Display one or many secrets."""
    pass


# ----------------------------------------------------------------- #
#                         Merge Subcommand                          #
# ----------------------------------------------------------------- #


@main.command("merge", cls=CustomCommand, epilog=MAIN_EPILOG)
@click.help_option("-h", "--help", hidden=True)
@click.option(
    "-f",
    "--filename",
    help="Target file of the merge.",
    metavar="",
)
@click.option(
    "-w",
    "--with-file",
    help="File to merge into target file.",
    metavar="",
)
@click.option(
    "-l",
    "--latest",
    help="Merge file with latest records using the value of lastTimestamp in"
    " metadata",
    metavar="",
)
def merge(filename, with_file=None, latest=None):
    """Merge FingerprintsGroups into SpyderbatBaselines and
    SpyderbatPolicies
    """
    pass


if __name__ == "__main__":
    main()
