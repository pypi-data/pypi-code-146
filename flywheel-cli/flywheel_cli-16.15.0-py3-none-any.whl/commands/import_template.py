"""Template Import Module"""
import argparse
import os
import re
import sys
import textwrap

from ruamel.yaml import YAML, YAMLError

from .. import util
from ..importers import FolderImporter, parse_template_list, parse_template_string
from ..util import METADATA_ALIASES, group_id, set_nested_attr, split_key_value_argument


def add_command(subparsers, parents):
    """Add commands for template import"""
    parser = subparsers.add_parser(
        "template",
        parents=parents,
        help="Import a folder, using a template",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description=textwrap.dedent(
            """\
            A template string can be used to extract metadata from custom folder trees.

            Simple properties can be extracted using replacement syntax; subfolders
            are delimited by ':'. For example:
                'ses-{session}-{subject}:{acquisition}'
            would extract the session label "01", subject code "ex2002" and
            acquisition label of "Diffusion" from the folder names:
                ses-01-ex2002/Diffusion

            Any variable can be set using --set-var. e.g. to set the acquisition label:
                --set-var 'acquisition.label=Scan'
        """
        ),
    )

    parser.add_argument(
        "--group",
        "-g",
        metavar="<id>",
        help="The id of the group, if not in folder structure",
        type=group_id,
    )
    parser.add_argument(
        "--project",
        "-p",
        metavar="<label>",
        help="The label of the project, if not in folder structure",
    )

    parser.add_argument(
        "--group-override",
        metavar="<id>",
        help="Force using this group id",
        type=group_id,
    )
    parser.add_argument(
        "--project-override", metavar="<label>", help="Force using this project label"
    )

    parser.add_argument(
        "--repack",
        action="store_true",
        help="Whether or not to validate, de-identify and repackage zipped packfiles",
    )

    no_level_group = parser.add_mutually_exclusive_group()
    no_level_group.add_argument(
        "--no-subjects",
        action="store_true",
        help="no subject level (create a subject for every session)",
    )
    no_level_group.add_argument(
        "--no-sessions",
        action="store_true",
        help="no session level (create a session for every subject)",
    )

    parser.add_argument(
        "--set-var",
        "-s",
        metavar="key=value",
        action="append",
        default=[],
        type=split_key_value_argument,
        help="Set arbitrary key-value pairs",
    )

    parser.add_argument("template", help="The template string")
    parser.add_argument("folder", help="The path to the folder to import")

    parser.set_defaults(func=import_folder_with_template)
    parser.set_defaults(parser=parser)

    return parser


def build_context(variables):
    """Context Builder For FolderImporter"""
    context = {}
    for key, value in variables:
        if key in METADATA_ALIASES:
            key = METADATA_ALIASES.get(key)
        set_nested_attr(context, key, value)
    return context


def import_folder_with_template(args):
    """Import with Template"""
    if args.config.output_folder is None:
        util.get_sdk_client_for_current_user().is_logged_in()

    # Build the importer instance
    importer = FolderImporter(
        group=args.group,
        project=args.project,
        repackage_archives=args.repack,
        merge_subject_and_session=(args.no_subjects or args.no_sessions),
        context=build_context(args.set_var),
        config=args.config,
        group_override=args.group_override,
        project_override=args.project_override,
    )  # pylint: disable=R0913

    if os.path.isfile(args.template):
        with open(args.template, "r", encoding="utf-8") as f:
            try:
                yaml = YAML()
                template_list = yaml.load(f)
                importer.root_node = parse_template_list(template_list, args.config)
            except YAMLError:
                print("Unable to parse template file (YAML expected)", file=sys.stderr)
                sys.exit(1)
    elif re.match(r".*\.ya?ml$", args.template, flags=re.IGNORECASE):
        print("Template file does not exist", file=sys.stderr)
        sys.exit(1)
    else:
        # Build the template string
        try:
            importer.root_node = parse_template_string(args.template, args.config)
        except (ValueError, re.error) as exc:
            args.parser.error(f"Invalid template: {exc}")

    # Check if template or args.group refer to group id
    if not args.group:
        node = importer.root_node
        while node:
            if hasattr(node, "template") and "group" in node.template.pattern:
                break
            node = getattr(node, "next_node", None)
        else:
            print("Group must be specified either in the template or using -g")
            sys.exit(1)

    # Perform the import
    importer.interactive_import(args.folder)
