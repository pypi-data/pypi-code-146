""" Providers Related Operations"""
import argparse
import json
import logging
import os
import sys
import tempfile

import flywheel
from ruamel.yaml import YAML, YAMLError

from .. import util

log = logging.getLogger(__name__)


def add_add_command(subparsers, parents):
    """Adds the 'add' tree of provider commands to the current command lineage"""
    parser = subparsers.add_parser(
        "add", parents=parents, help="Add a new provider into Flywheel"
    )
    # We have to replicate these arguments to all the subparses to keep the command positional order sane
    # parser.add_argument('--label', required=False, help='Name of the provider')
    # parser.add_argument('--skip-edit', required=False, help='Skip the interactive editor', action='store_true')

    def print_help(args):  # pylint: disable=unused-argument
        parser.print_help()

    parser.set_defaults(func=print_help)
    subparsers = parser.add_subparsers(dest="class_")

    add_class_commands(subparsers, parents)

    return parser


def add_modify_command(subparsers, parents):
    """Adds the 'mod' tree of provider commands to the current command lineage."""
    parser = subparsers.add_parser(
        "modify",
        parents=parents,
        help="Modify the configuration of a provider in Flywheel",
    )

    parser.add_argument("id", help="A string with the provider id")
    parser.set_defaults(func=mod_provider)

    # The args are parseed for all command so to allow unkwown commands would required enabling that on the entire tree
    # Instead just add all the possible args and suppress the notice so they are hidden but validated if supplied
    parser.add_argument(
        "--skip-edit", required=False, action="store_true", help=argparse.SUPPRESS
    )
    parser.add_argument("--label", required=False, help=argparse.SUPPRESS)
    parser.add_argument(
        "--aws-secret-access-key", required=False, help=argparse.SUPPRESS
    )
    parser.add_argument("--aws-access-key-id", required=False, help=argparse.SUPPRESS)
    parser.add_argument("--gs-json-key-file", required=False, help=argparse.SUPPRESS)
    parser.add_argument("--region", required=False, help=argparse.SUPPRESS)
    parser.add_argument("--path", required=False, help=argparse.SUPPRESS)
    parser.add_argument("--bucket", required=False, help=argparse.SUPPRESS)
    parser.add_argument("--queue-threshold", required=False, help=argparse.SUPPRESS)
    parser.add_argument("--max-compute", required=False, help=argparse.SUPPRESS)
    parser.add_argument("--machine-type", required=False, help=argparse.SUPPRESS)
    parser.add_argument("--disk-size", required=False, help=argparse.SUPPRESS)
    parser.add_argument("--swap-size", required=False, help=argparse.SUPPRESS)
    parser.add_argument("--preemptible", required=False, help=argparse.SUPPRESS)
    parser.add_argument("--zone", required=False, help=argparse.SUPPRESS)

    return parser


def add_class_commands(subparsers, parents):
    """Adds class command as a subparser to the chain"""

    parser_compute = subparsers.add_parser(
        "compute", help="Compute provider type", parents=parents
    )

    def print_compute_help(args):  # pylint: disable=unused-argument
        parser_compute.print_help()

    parser_compute.set_defaults(func=print_compute_help)

    compute_subs = parser_compute.add_subparsers(dest="type", metavar="{type}")
    add_compute_type_commands(compute_subs, parents)

    parser_storage = subparsers.add_parser(
        "storage", help="Storage Provider Class", parents=parents
    )

    def print_storage_help(args):  # pylint: disable=unused-argument
        parser_storage.print_help()

    parser_storage.set_defaults(func=print_storage_help)
    storage_subs = parser_storage.add_subparsers(dest="type", metavar="{type}")
    add_storage_type_commands(storage_subs, parents)


def add_storage_type_commands(subparsers, parents):
    """Adds storage class commands and arguments to the subparser chain"""
    parser_aws = subparsers.add_parser("aws", help="Aws type provider", parents=parents)
    parser_aws.set_defaults(func=add_provider)
    # TODO: We need the arg at this level if we want them in sequence positionally
    parser_aws.add_argument("--label", required=False, help="Name of the provider")
    parser_aws.add_argument(
        "--skip-edit",
        required=False,
        help="Skip the interactive editor",
        action="store_true",
    )
    add_aws_creds(parser_aws)
    add_aws_storage_config(parser_aws)

    parser_gc = subparsers.add_parser(
        "gc", help="Google Cloud provider", parents=parents
    )
    parser_gc.set_defaults(func=add_provider)
    parser_gc.add_argument("--label", required=False, help="Name of the provider")
    parser_gc.add_argument(
        "--skip-edit",
        required=False,
        help="Skip the interactive editor",
        action="store_true",
    )
    add_gc_creds(parser_gc)
    add_gc_storage_config(parser_gc)

    parser_local = subparsers.add_parser("local", parents=parents)
    parser_local.set_defaults(func=add_provider)
    parser_local.add_argument("--label", required=False, help="Name of the provider")
    parser_local.add_argument(
        "--skip-edit",
        required=False,
        help="Skip the interactive editor",
        action="store_true",
    )
    add_local_storage_config(parser_local)


def add_compute_type_commands(subparsers, parents):
    """Adds compute  class commands and arguments to the subparser chain"""
    parser_aws = subparsers.add_parser("aws", help="Aws type provider", parents=parents)
    parser_aws.set_defaults(func=add_provider)
    parser_aws.add_argument("--label", required=False, help="Name of the provider")
    parser_aws.add_argument(
        "--skip-edit",
        required=False,
        help="Skip the interactive editor",
        action="store_true",
    )
    add_aws_creds(parser_aws)
    add_compute_config(parser_aws)

    parser_gc = subparsers.add_parser(
        "gc", help="Google Cloud Compute provider", parents=parents
    )
    parser_gc.set_defaults(func=add_provider)
    parser_gc.add_argument("--label", required=False, help="Name of the provider")
    parser_gc.add_argument(
        "--skip-edit",
        required=False,
        help="Skip the interactive editor",
        action="store_true",
    )
    add_gc_creds(parser_gc)
    add_compute_config(parser_gc)

    parser_static = subparsers.add_parser("static", parents=parents)
    parser_static.add_argument("--label", required=False, help="Name of the provider")
    parser_static.add_argument(
        "--skip-edit",
        required=False,
        help="Skip the interactive editor",
        action="store_true",
    )
    parser_static.set_defaults(func=add_provider)
    add_compute_config(parser_static)


def add_aws_creds(parser):
    """Adds AWS cred arguemnts"""
    parser.add_argument(
        "--aws-secret-access-key", required=False, help="AWS secret access key"
    )
    parser.add_argument("--aws-access-key-id", required=False, help="AWS access key id")


def add_gc_creds(parser):
    """Adds GC cred arguemnts"""
    parser.add_argument(
        "--gs-json-key-file",
        required=False,
        help="location of the Google Cloud key.json file",
    )


def add_aws_storage_config(parser):
    """Adds AWS storage arguemnts"""
    parser.add_argument("--region", required=False, help="AWS region")
    parser.add_argument("--path", required=False, help="AWS Storge path")
    parser.add_argument("--bucket", required=False, help="AWS bucket name")


def add_gc_storage_config(parser):
    """Adds GC stroage arguments"""
    parser.add_argument("--region", required=False, help="GC Storage region")
    parser.add_argument("--path", required=False, help="GC Storge path")
    parser.add_argument("--bucket", required=False, help="GC bucket name")


def add_local_storage_config(parser):
    """Adds local storage config"""
    parser.add_argument("--path", required=False, help="Local Storge path")


def add_compute_config(parser):
    """Adds common compute arguments to the parser"""
    parser.add_argument("--queue-threshold", help="Queue threshold for the provider")
    parser.add_argument("--max-compute", help="Queue threshold for the provider")
    parser.add_argument("--machine-type", help="Machine Type for the provider")
    parser.add_argument(
        "--disk-size", help="Disk Size for the provider in MB"
    )  # TODO: whare are the unit here?
    parser.add_argument(
        "--swap-size", help="Swap Size for the provider, string ie. 30G"
    )
    parser.add_argument("--preemptible", help="Create a preemtible provider")
    parser.add_argument("--zone", help="Zone to use for this provider")
    parser.add_argument("--region", help="Region to use for this provider")


def add_assign_command(subparsers, parents):
    """Creates the assignement provider command"""
    parser = subparsers.add_parser(
        "assign",
        parents=parents,
        help="Modify the configuration of a provider in Flywheel",
    )
    parser.add_argument(
        "type",
        help="The container type to which you want to assign providers.",
        choices=["site", "group", "project"],
    )
    parser.add_argument("id", help="Id of the container to assign providers", nargs="?")
    parser.add_argument(
        "--compute",
        metavar="ID",
        required=False,
        help="Provider id to assign as the compute provider",
    )
    parser.add_argument(
        "--storage",
        metavar="ID",
        required=False,
        help="Provider id to assign as the storage provider",
    )
    parser.add_argument(
        "--change-log",
        metavar="ID",
        required=False,
        help="Provider id to assign as the changelog provider",
    )
    parser.add_argument(
        "--job-logs",
        metavar="ID",
        required=False,
        help="Set the site provider for cold storage of job logs",
    )
    parser.set_defaults(func=assign_provider)
    parser.set_defaults(parser=parser)
    return parser


def add_provider(args):  # pylint: disable=inconsistent-return-statements
    """Actual data processing routing for adding providers.  All sub command route through this
    function so we do need to check for which optional arguments are supplied.
    """
    fw = util.get_sdk_client_for_current_user()
    config = get_config_vals(class_=args.class_, type_=args.type)

    parse_args(args, config)

    if args.skip_edit:
        id_ = fw.add_provider(config)
        # log.info(f'Provider has been saved: {id_}')
        return id_
    process_edit(config, fw.add_provider)


def mod_provider(args):
    """Providers the data processing for provider modification
    We only allow changing of the label, config, and creds.
    """
    fw = util.get_sdk_client_for_current_user()

    try:
        provider = fw.get_provider(args.id)
    except flywheel.ApiException as exc:
        log.error(str(exc))
        sys.exit(1)

    mod_data = {
        "label": provider.label,
        "config": provider.config if provider.config else {},
    }
    parse_args(args, mod_data)

    if provider.creds:
        mod_data["creds"] = provider.creds

    if args.skip_edit:
        fw.modify_provider(args.id, mod_data)
    else:
        process_edit(mod_data, fw.modify_provider, args.id)


def assign_provider(args):
    """Actual processing of provider assignment command"""
    if args.type == "site":
        if hasattr(args, "id") and args.id is not None:
            log.error("You must not specify an ID for site")
            sys.exit(1)
    else:
        if not hasattr(args, "id") or args.id is None:
            log.error(f"You must specify an ID for {args.type}")
            sys.exit(1)

    def check_container(args, storage_type, valid_types):
        if args.type not in valid_types:
            log.error(
                f"{storage_type} provider can be set for {' and '.join(valid_types)} only"
            )
            sys.exit(1)

    data = {"providers": {}}

    has_provider = False
    if hasattr(args, "storage") and args.storage:
        check_container(args, "storage", ["group", "project"])
        data["providers"]["storage"] = args.storage
        has_provider = True
    if hasattr(args, "compute") and args.compute:
        check_container(args, "compute", ["group", "project"])
        data["providers"]["compute"] = args.compute
        has_provider = True
    if hasattr(args, "change_log") and args.change_log:
        check_container(args, "change_log", ["site"])
        data["providers"]["change_log"] = args.change_log
        has_provider = True
    if hasattr(args, "job_logs") and args.job_logs:
        check_container(args, "job_logs", ["site"])
        data["providers"]["job_logs"] = args.job_logs
        has_provider = True

    if not has_provider:
        log.error("You must provider either a Storage, Compute or Changelog provider")
        sys.exit(1)

    fw = util.get_sdk_client_for_current_user()
    try:
        if args.type == "group":
            fw.modify_group(args.id, data)
        if args.type == "project":
            fw.modify_project(args.id, data)
        if args.type == "site":
            fw.modify_site_settings(data)
    except flywheel.ApiException as exc:
        log.error(str(exc))
        sys.exit(1)

    log.info(f"{args.type} was saved.")


def process_edit(config, function, id_=None):
    """Provides a local system editor that allows the user to view the config in Yaml.
    Usees the current api to validate changes so that we can determine when the configuration
    is correct and complete otherwise we look the user in the edit routine, unless user exits.

    args:
        config dictionary: The current object config to be injected
        function function: The callable sdk command to process the data
        id string: The id if we are going to be editing an existing provider
    """
    yaml = YAML()

    fd, path = tempfile.mkstemp("provider-config")
    with os.fdopen(fd, "w") as f:
        print("# Edit this file and then save and exit to save the provider.", file=f)
        yaml.dump(config, f)

    valid = False
    while not valid:

        util.edit_file(path)
        try:
            with open(path, encoding="utf-8") as fp:
                data = yaml.load(fp)
        except (IOError, YAMLError) as exc:
            log.error(str(exc))
            choice = input(
                "\nInvalid YAML. Enter 'q' to quit. Or press any other key to re-edit the configuration\n"
            )
            if choice in ("q", "Q"):
                log.info("Provider has not been saved")
                sys.exit(1)
            continue

        try:
            if id_ is not None:
                # On modify we only get a 200 back and no response data
                function(id_, data)
            else:
                provider = function(data)
        except flywheel.ApiException as exc:
            log.error(str(exc))

            choice = input(
                "\nEnter 'q' to quit. Or press any other key to re-edit the configuration\n"
            )
            if choice in ("q", "Q"):
                log.info("Provider has not been saved")
                sys.exit(1)
            continue

        valid = True

    if id_:
        log.info(f"Provider has been saved: {id_}")
    else:
        log.info(f"Provider has been saved: {provider}")


def parse_args(args, config):  # pylint: disable=too-many-branches
    """
    Pull args off the command line and place them in the respective config locations
    """

    if hasattr(args, "aws_secret_access_key") and args.aws_secret_access_key:
        config["creds"]["aws_secret_access_key"] = args.aws_secret_access_key
    if hasattr(args, "aws_access_key_id") and args.aws_access_key_id:
        config["creds"]["aws_access_key_id"] = args.aws_access_key_id

    if hasattr(args, "label") and args.label:
        config["label"] = args.label
    if hasattr(args, "path") and args.path:
        config["config"]["path"] = args.path
    if hasattr(args, "region") and args.region:
        config["config"]["region"] = args.region
    if hasattr(args, "bucket") and args.bucket:
        config["config"]["bucket"] = args.bucket
    if hasattr(args, "zone") and args.zone:
        config["config"]["zone"] = args.zone
    if hasattr(args, "queue_threshold") and args.queue_threshold:
        config["config"]["queue_threshold"] = args.queue_threshold
    if hasattr(args, "max_compute") and args.max_compute:
        config["config"]["max_compute"] = args.max_compute
    if hasattr(args, "machine_type") and args.machine_type:
        config["config"]["machine_type"] = args.machine_type
    if hasattr(args, "disk_size") and args.disk_size:
        config["config"]["disk_size"] = args.disk_size
    if hasattr(args, "swap_size") and args.swap_size:
        config["config"]["swap_size"] = args.swap_size
    if hasattr(args, "preemptible"):
        config["config"]["preemptible"] = args.preemptible

    if hasattr(args, "gs_json_key_file") and args.gs_json_key_file:
        with open(args.gs_json_key_file, "r", encoding="utf-8") as f:
            key = json.load(f)
            config["creds"]["client_email"] = key["client_email"]
            config["creds"]["client_id"] = key["client_id"]
            config["creds"]["project_id"] = key["project_id"]
            config["creds"]["private_key_id"] = key["private_key_id"]
            config["creds"]["private_key"] = key["private_key"]
            config["creds"]["client_x509_cert_url"] = key["client_x509_cert_url"]
            config["creds"]["auth_provider_x509_cert_url"] = key[
                "auth_provider_x509_cert_url"
            ]
            config["creds"]["token_uri"] = key["token_uri"]
            config["creds"]["auth_uri"] = key["auth_uri"]
            config["creds"]["type"] = key["type"]


def get_config_vals(class_, type_):
    """
    Provides a configuration dict that has all the needed fields for the specified type and class
    so that data can be injected into this dic to present to the user.
    """

    return_vals = {"provider_class": class_, "provider_type": type_, "label": ""}

    # All compute need base values
    if class_ == "compute":
        return_vals["config"] = {
            "region": "",
            "zone": "",
            "queue_threshold": 1,
            "max_compute": 1,
            "machine_type": 1,
            "disk_size": 100,
            "swap_size": "30G",
            "preemptible": False,
        }

    # These are the non creds types
    if class_ == "storage" and type_ == "local":
        return_vals["config"] = {"path": ""}
        return_vals["creds"] = {}
        return return_vals

    if class_ == "compute" and type_ == "static":
        return_vals["creds"] = {}
        return return_vals

    ## Below are the creds versions

    if type_ == "gc":
        return_vals["creds"] = {
            "client_email": "",
            "client_id": "",
            "project_id": "",
            "private_key": "",
            "private_key_id": "",
            "client_x509_cert_url": "",
            "auth_provider_x509_cert_url": "",
            "auth_uri": "",
            "token_uri": "",
            "type": "",
        }

    # Aws types use the same creds
    if type_ == "aws":
        return_vals["creds"] = {"aws_access_key_id": "", "aws_secret_access_key": ""}
    if class_ == "storage":
        return_vals["config"] = {"bucket": "", "region": "", "path": ""}
        return return_vals

    return return_vals
