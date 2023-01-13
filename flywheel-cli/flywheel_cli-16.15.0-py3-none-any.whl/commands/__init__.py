""" Initializing Commands Module"""
import os

import crayons

from .. import util
from ..config import Config
from . import (
    deid,
    essentials,
    export_bids,
    gears,
    import_bids,
    import_bruker,
    import_dicom,
    import_folder,
    import_parrec,
    import_template,
    ingest,
    retry_job,
    sync,
)


def set_subparser_print_help(parser, subparsers):
    """Set subcommands help"""

    def print_subcommands_help(args):  # pylint: disable=unused-argument
        parser.print_help()

    parser.set_defaults(func=print_subcommands_help)

    help_parser = subparsers.add_parser("help", help="Print this help message and exit")
    help_parser.set_defaults(func=print_subcommands_help)


def print_help(default_parser, parsers):
    """Print commands help"""

    def print_help_fn(args):
        subcommands = " ".join(args.subcommands)
        if subcommands in parsers:
            parsers[subcommands].print_help()
        else:
            default_parser.print_help()

    return print_help_fn


def get_config(args):
    """Get config"""
    args.config = Config(args)


def add_commands(parser):
    """Init adding commands"""
    # pylint: disable=too-many-locals,too-many-statements
    # Setup global configuration args
    parser.set_defaults(config=get_config)

    global_parser = Config.get_global_parser()
    import_parser = Config.get_import_parser()
    deid_parser = Config.get_deid_parser()

    user_config = util.load_auth_config()

    # Command switches:
    enable_beta_commands = os.environ.get("FLYWHEEL_CLI_BETA") == "true"
    enable_legacy_commands = os.environ.get("FLYWHEEL_CLI_LEGACY") == "true"
    enable_admin = user_config.get("root", False)

    # map commands for help function
    parsers = {}

    # Create subparsers
    subparsers = parser.add_subparsers(title="Available commands", metavar="")

    # =====
    # Essentials
    # =====
    essentials.add_commands(subparsers, parsers, parents=[global_parser])
    # =====
    # import
    # =====
    parser_import = subparsers.add_parser(
        "import",
        help="Import data into Flywheel"
        if enable_legacy_commands
        else "[Deprecated] - please use `fw ingest` instead",
    )

    if enable_legacy_commands:
        parser_import = subparsers.add_parser(
            "import", help="Import data into Flywheel"
        )
        parsers["import"] = parser_import

        import_subparsers = parser_import.add_subparsers(
            title="Available import commands", metavar=""
        )

        # import folder
        parsers["import folder"] = import_folder.add_command(
            import_subparsers, [global_parser, import_parser, deid_parser]
        )

        # import bids
        parsers["import bids"] = import_bids.add_command(
            import_subparsers, [global_parser]
        )

        # import dicom
        parsers["import dicom"] = import_dicom.add_command(
            import_subparsers, [global_parser, import_parser, deid_parser]
        )

        # import bruker
        parsers["import bruker"] = import_bruker.add_command(
            import_subparsers, [global_parser, import_parser]
        )

        # import parrec
        parsers["import parrec"] = import_parrec.add_command(
            import_subparsers, [global_parser, import_parser]
        )

        # import template
        parsers["import template"] = import_template.add_command(
            import_subparsers, [global_parser, import_parser, deid_parser]
        )
        # Link help commands
        set_subparser_print_help(parser_import, import_subparsers)
    else:
        parser_import.set_defaults(func=import_depr)

    # =====
    # export
    # =====
    parser_export = subparsers.add_parser("export", help="Export data from Flywheel")
    parsers["export"] = parser_export

    export_subparsers = parser_export.add_subparsers(
        title="Available export commands", metavar=""
    )

    parsers["export bids"] = export_bids.add_command(export_subparsers, [global_parser])

    # Link help commands
    set_subparser_print_help(parser_export, export_subparsers)

    # =====
    # job
    # =====
    parser_job = subparsers.add_parser("job", help="Start or manage server jobs")
    parser_job.set_defaults(config=get_config)
    parsers["job"] = parser_job

    job_subparsers = parser_job.add_subparsers(
        title="Available job commands", metavar=""
    )

    parsers["job retry"] = retry_job.add_command(job_subparsers, [global_parser])

    # Link help commands
    set_subparser_print_help(parser_job, job_subparsers)

    # =====
    # sync
    # =====
    parsers["sync"] = sync.add_command(subparsers, [global_parser])

    # =====
    # ingest
    # =====
    parser_ingest = subparsers.add_parser("ingest", help="Ingest data")
    parser_ingest.set_defaults(skip_load_defaults=True)
    parsers["ingest"] = parser_ingest
    ingest_subparsers = parser_ingest.add_subparsers(
        title="Available ingest commands", metavar=""
    )
    ingest.add_commands(ingest_subparsers)
    # Link help commands
    set_subparser_print_help(parser_ingest, ingest_subparsers)

    # =====
    # deid
    # =====
    parser_deid = subparsers.add_parser(
        "deid",
        help="Test your de-identification template or generate a sample template",
    )
    parser_deid.set_defaults(skip_load_defaults=True)
    parsers["deid"] = parser_deid
    deid_subparsers = parser_deid.add_subparsers(
        title="Available deid commands", metavar=""
    )
    deid.add_commands(deid_subparsers)
    # Link help commands
    set_subparser_print_help(parser_deid, deid_subparsers)

    # =====
    # Admin Commands
    # =====
    if enable_admin:
        parser_admin = subparsers.add_parser(
            "admin", help="Site administration commands"
        )
        parser_admin.set_defaults(config=get_config)
        parsers["admin"] = parser_admin

        admin_subparsers = parser_admin.add_subparsers(
            title="Available admin commands", metavar=""
        )
    else:
        parser_admin = None
        admin_subparsers = None

    if parser_admin is not None:
        # =====
        # providers
        # =====
        from . import providers  # pylint: disable=import-outside-toplevel

        parser_provider = admin_subparsers.add_parser(
            "provider", help="Add/Modify/Assign providers in the Flywheel system"
        )
        parser_provider.set_defaults(config=get_config)
        parsers["admin provider"] = parser_provider

        provider_subparsers = parser_provider.add_subparsers(
            title="Available provider commands", metavar=""
        )
        parsers["admin provider add"] = providers.add_add_command(
            provider_subparsers, []
        )
        parsers["admin provider modify"] = providers.add_modify_command(
            provider_subparsers, []
        )
        parsers["admin provider assign"] = providers.add_assign_command(
            provider_subparsers, []
        )

        # Link help commands
        set_subparser_print_help(parser_provider, provider_subparsers)

        # =====
        # Editions
        # =====
        from . import editions  # pylint: disable=import-outside-toplevel

        parser_edition = admin_subparsers.add_parser(
            "edition", help="Enable/disable an edtion on a group/project"
        )
        parser_edition.set_defaults(config=get_config)

        edition_subparsers = parser_edition.add_subparsers(
            title="Available edition commands", metavar=""
        )
        parsers["admin edition enable"] = editions.add_enable_command(
            edition_subparsers, []
        )
        parsers["admin edition disable"] = editions.add_disable_command(
            edition_subparsers, []
        )

        # Link help commands
        set_subparser_print_help(parser_provider, edition_subparsers)

        # =====
        # Gears
        # =====

        parser_gears = admin_subparsers.add_parser(
            "gears", help="Manage gears installed on flywheel instances"
        )
        parsers["admin gears"] = parser_gears

        gears_subparsers = parser_gears.add_subparsers(
            title="Available gears commands", metavar=""
        )
        set_subparser_print_help(parser_gears, gears_subparsers)

        parsers["admin gear enable"] = gears.gears_enable.add_command(gears_subparsers)
        parsers["admin gear disable"] = gears.gears_disable.add_command(
            gears_subparsers
        )

        if enable_beta_commands:
            parsers["admin gears install"] = gears.gears_install.add_command(
                gears_subparsers
            )
            parsers["admin gears upgrade"] = gears.gears_upgrade.add_command(
                gears_subparsers
            )
            parsers["admin gears show"] = gears.gears_show.add_command(gears_subparsers)
            parsers["admin gears list"] = gears.gears_list.add_command(gears_subparsers)
            parsers["admin gears search"] = gears.gears_search.add_command(
                gears_subparsers
            )

            parser_rules = admin_subparsers.add_parser(
                "gear-rules", help="Manage gear-rules on flywheel instances"
            )
            parsers["admin gears-rules"] = parser_rules

            rules_subparsers = parser_rules.add_subparsers(
                title="Available gear-rules commands", metavar=""
            )
            set_subparser_print_help(parser_rules, rules_subparsers)
            parsers["admin gear-rules list"] = gears.rules_list.add_command(
                rules_subparsers
            )
            parsers["admin gears-rules upgrade"] = gears.rules_upgrade.add_command(
                rules_subparsers
            )

    # =====
    # help commands
    # =====
    parser_help = subparsers.add_parser("help")
    parser_help.add_argument("subcommands", nargs="*")
    parser_help.set_defaults(func=print_help(parser, parsers))
    Config.set_defaults(parsers)


def import_depr(args):
    # pylint: disable=unused-argument
    """Import"""
    print(
        crayons.red(
            "The import command has been replaced by the ingest command and will be removed in a future release."
            "\n\nRefer to https://docs.flywheel.io/hc/en-us/articles/4416119193491 for details."
        )
    )
