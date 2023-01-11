import json
import os
import re
import sys

sys.path.append(
    os.path.dirname(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    )
)

from string import Template

import click

from truera.artifactrepo.arlib import artifactrepolib as arlib
from truera.client.private import metarepo as mr
from truera.utils.check_permission_helper import MOCK_REQUEST_CONTEXT

# This CLI is meant for the dev / onebox scenario to facilitate pre-loading cached computations
# and metadata. The intended use is for us to be able to dump a json after caches are all computed
# and include that with the repository, then to be able to re-insert all those caches on a
# different machine with a different $AILENS_REPO_HOME.
# Sample command lines:
#
# > python truera/utils/cache_dump_and_reload_util.py dump-meta-repo-cache-tables --output_path /home/cache_dump_demo_proj
#
# > python truera/utils/cache_dump_and_reload_util.py load-meta-repo-cache-tables --input_path /home/cache_dump_demo_proj --exclude_table dataset
#
# > python truera/utils/cache_dump_and_reload_util.py load-meta-repo-cache-tables --input_path /home/cache_dump_demo_proj --load_project adult --load_table SEGMENTATION


@click.group()
def cache_dump_reload_cli():
    pass


@cache_dump_reload_cli.command()
@click.option(
    "--output_path",
    help="Output directory for the processed json of the cache tables."
)
@click.option(
    "--connection_string",
    help="Connection string to truera endpoint.",
    default="http://localhost:9290"
)
@click.option(
    "--fixup",
    nargs=2,
    help=
    "Takes two arguments: one for string to find, the other to replace it with.",
    multiple=True
)
def dump_meta_repo_cache_tables(output_path, fixup, connection_string):
    ailens_repo_home_val = os.environ["AILENS_REPO_HOME"]
    print("$AILENS_REPO_HOME=" + ailens_repo_home_val)
    with mr.MetaRepo(connection_string) as metarepo:
        default_table_list = metarepo.get_entity_names(
            request_ctx=MOCK_REQUEST_CONTEXT
        )
        os.makedirs(output_path, exist_ok=False)

        # Entities that have project_id in the top level get written to:
        # output_dir/project_specific_data/<project_id>/<table_name>/id
        project_data_dir_name = "project_specific_data"
        os.makedirs(os.path.join(output_path, project_data_dir_name))

        for table_name in default_table_list:
            entities = metarepo.get_entities(
                request_ctx=MOCK_REQUEST_CONTEXT, entity=table_name
            )
            entities_not_attached_to_project = []

            full_contents = replace_env_var_for_output(
                json.dumps(entities, indent=2, sort_keys=True),
                ailens_repo_home_val
            )
            print(table_name + " CONTENTS:")
            print(full_contents)

            for entity in entities:
                project_id = get_project_id_if_present(entity, table_name)
                if not project_id:
                    entities_not_attached_to_project.append(entity)
                    continue

                entity_output_dir = os.path.join(
                    output_path, project_data_dir_name, project_id, table_name
                )
                os.makedirs(entity_output_dir, exist_ok=True)

                contents = replace_env_var_for_output(
                    json.dumps(entity, indent=2, sort_keys=True),
                    ailens_repo_home_val
                )
                with open(
                    escape_path(
                        os.path.join(entity_output_dir, entity.get('id'))
                    ), "w"
                ) as fp:
                    do_write(fp, contents, fixup)

            if entities_not_attached_to_project:
                spillover_contents = replace_env_var_for_output(
                    json.dumps(
                        entities_not_attached_to_project,
                        indent=2,
                        sort_keys=True
                    ), ailens_repo_home_val
                )

                with open(os.path.join(output_path, table_name), "w") as fp:
                    do_write(fp, contents, fixup)

    print("Done")


def do_write(fp, contents, fixups):
    for fixup in fixups:
        contents = contents.replace(fixup[0], fixup[1])
    fp.write(contents)


@cache_dump_reload_cli.command()
@click.option(
    "--input_path",
    help="Input directory for the processed json of the cache tables."
)
@click.option("--load_table", multiple=True)
@click.option("--exclude_table", multiple=True)
@click.option(
    "--load_project",
    nargs=2,
    multiple=True,
    help=
    "For project specific entitites, we only load metadata for the specified projects. Takes two parts, the name and the id. If none are specified all projects are loaded."
)
@click.option(
    "--skip_entities",
    nargs=2,
    multiple=True,
    help=
    "Takes two parts: X and Y. Allows for skipping entities in table X with name Y."
)
@click.option(
    "--connection_string",
    help="Connection string to truera endpoint.",
    default="http://localhost:9290"
)
def load_meta_repo_cache_tables(
    input_path, load_table, exclude_table, load_project, skip_entities,
    connection_string
):
    ailens_repo_home_val = os.environ["AILENS_REPO_HOME"]
    print("$AILENS_REPO_HOME=" + ailens_repo_home_val)
    print(f"Skipping entities named: {skip_entities}")
    with mr.MetaRepo(connection_string) as metarepo:
        default_table_list = metarepo.get_entity_names(
            request_ctx=MOCK_REQUEST_CONTEXT
        )

        # get consistent behavior for load & exclude lists regardless of casing
        # note that projects don't have this done since you can have two projects
        # with the same id but different casing.
        load_table = [x.lower() for x in load_table]
        exclude_table = [x.lower() for x in exclude_table]

        print("Specified load tables:" + str(load_table))
        print("Specified excluded tables: " + str(exclude_table))

        print("Loading general tables...")
        table_list = []
        project_name_list = []
        project_name_id_map = {}

        for t in load_table:
            if t not in exclude_table:
                table_list.append(t)

        if table_list == []:
            table_list = [
                table for table in default_table_list
                if table not in exclude_table
            ]

        for p in load_project:
            project_name_list.append(p[0])
            project_name_id_map[p[0]] = p[1]

        skip_entities_named = {}
        for table, name in skip_entities:
            if table in skip_entities_named:
                skip_entities_named[table].add(name)
            else:
                skip_entities_named[table] = [name]

        for table_name in table_list:
            print("Loading " + table_name + "...")

            table_file = os.path.join(input_path, table_name)
            if not os.path.isfile(table_file):
                print(
                    f"Table {table_name} does not exist as a general (not project specific) table in the specified directory: {table_file}."
                )
                continue

            with open(table_file, "r") as fp:
                contents = fp.read()
            contents = replace_env_var_for_input(contents, ailens_repo_home_val)

            entities = json.loads(contents)

            for e in entities:
                if "name" in e and table_name.lower(
                ) in skip_entities_named and e["name"] in skip_entities_named[
                    table_name.lower()]:
                    print(
                        f"Skipped entity in table {table_name} named {e['name']}"
                    )
                    continue
                metarepo.put_entity(
                    request_ctx=MOCK_REQUEST_CONTEXT, entity=table_name, body=e
                )

        print("Loading project specific tables...")
        project_specific_data_path = os.path.join(
            input_path, "project_specific_data"
        )
        if not os.path.isdir(project_specific_data_path):
            print(
                f"No project specific data found at {project_specific_data_path}."
            )
        else:
            for relative_path, full_path in arlib.flatten(
                project_specific_data_path, None
            ):
                # The relative paths have the form: <project id>/<table name>/<id>
                split = relative_path.split('/')

                # If splits are deleted this file is left around on Mac and breaks our decompisition logic
                if '.DS_Store' in split:
                    continue

                assert len(split) == 3
                project_name = split[0]
                table_name = split[1]
                entity_id = unescape_path(split[2])

                # if it isn't one of the specified projects continue
                if project_name_list and (
                    not project_name in project_name_list
                ):
                    continue

                # If it is the projects table, grab some details and augment the entries that should already
                # exist.
                if table_name == "project" and "project" not in load_table:
                    with open(full_path, "r") as fp:
                        contents = json.loads(fp.read())
                    if "documentation" in contents.keys():
                        project_md = metarepo.get_entity(
                            request_ctx=MOCK_REQUEST_CONTEXT,
                            entity="project",
                            entity_id=project_name_id_map[project_name]
                        )
                        project_md["documentation"] = contents["documentation"]
                        metarepo.put_entity(
                            request_ctx=MOCK_REQUEST_CONTEXT,
                            entity=table_name,
                            body=project_md
                        )
                    continue

                # if it is explicitly excluded or isn't one of the specified tables continue
                if (table_name.lower() in exclude_table
                   ) or (load_table and not table_name.lower() in load_table):
                    continue

                with open(full_path, "r") as fp:
                    contents = fp.read()

                replacements = {
                    "AILENS_REPO_HOME": ailens_repo_home_val,
                    "TRUERA_PROJECT_ID": project_name_id_map[project_name],
                    "{TRUERA_PROJECT_ID}": project_name_id_map[project_name]
                }
                contents = Template(contents).safe_substitute(replacements)

                entity = json.loads(contents)

                if "name" in entity and table_name.lower(
                ) in skip_entities_named and entity[
                    "name"] in skip_entities_named[table_name.lower()]:
                    print(
                        f"Skipped entity in table {table_name} named {entity['name']}"
                    )
                    continue

                metarepo.put_entity(
                    request_ctx=MOCK_REQUEST_CONTEXT,
                    entity=table_name,
                    body=entity
                )
                print("Loaded entity from path " + relative_path + ".")

    print("Done")


def get_project_id_if_present(entity, table_name):
    if table_name.lower() == "project":
        return entity.get('id')
    #option 2 - project_id is in the entity:
    project_id = entity.get('project_id')
    if project_id:
        return project_id
    model_id = entity.get('model_id')
    #option 3 - model_id.project_id is in the entity:
    if model_id:
        project_id = model_id.get('project_id')
        if project_id:
            return project_id

    return None


def replace_env_var_for_output(str_to_replace, repo_home_val):
    return str_to_replace.replace(repo_home_val, "$AILENS_REPO_HOME")


def replace_env_var_for_input(str_to_replace, repo_home_val):
    return str_to_replace.replace("$AILENS_REPO_HOME", repo_home_val)


# The escape / unescape process is required because we use "*" in id's sometimes, and
# this is not valid for paths on windows. If we even want to check out the code on windows
# then we cannot create paths with * in them.
def escape_path(path_to_escape):
    return path_to_escape.replace("*", "(astr)")


def unescape_path(path_to_escape):
    return path_to_escape.replace("(astr)", "*")


if __name__ == '__main__':
    cache_dump_reload_cli()
