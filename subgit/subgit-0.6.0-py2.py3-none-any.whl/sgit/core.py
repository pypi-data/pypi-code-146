# -*- coding: utf-8 -*-

# python std lib
import logging
import os
import re
import sys

# sgit imports
from sgit.constants import *
from sgit.enums import *
from sgit.exceptions import *

# 3rd party imports
import git
from git import Repo, Git
from packaging import version
from packaging.specifiers import SpecifierSet
from packaging.version import Version
from ruamel import yaml
from ruamel.yaml import Loader


logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)


class Sgit():
    def __init__(self, config_file_path=None, answer_yes=False):
        self.answer_yes = answer_yes

        if not config_file_path:
            self.sgit_config_file_name = ".sgit.yml"

            self.sgit_config_file_path = os.path.join(
                os.getcwd(), self.sgit_config_file_name
            )
        else:
            self.sgit_config_file_name = os.path.basename(config_file_path)
            self.sgit_config_file_path = config_file_path

    def init_repo(self):
        """
        Algorithm:
            - Check if .sgit.yml exists
                - If exists:
                    - Exit out from script
                - If do not exists
                    - Write new initial empty file to disk
        """
        if os.path.exists(self.sgit_config_file_path):
            print(f"File '{self.sgit_config_file_name}' already exists on disk")
            return 1

        with open(self.sgit_config_file_path, "w") as stream:
            stream.write(DEFAULT_REPO_CONTENT)
            print(f'Successfully wrote new config file "{self.sgit_config_file_name}" to disk')

    def _get_config_file(self):
        if not os.path.exists(self.sgit_config_file_path):
            print("No .sgit.yml file exists in current CWD")
            sys.exit(1)

        with open(self.sgit_config_file_path, "r") as stream:
            return yaml.load(stream, Loader=Loader)
            # TODO: Minimal required data should be 'repos:'
            #       Raise error if missing from loaded config

    def _dump_config_file(self, config_data):
        """
        Writes the entire config file to the given disk path set
        in the method constructor.
        """
        with open(self.sgit_config_file_path, "w") as stream:
            yaml.dump(config_data, stream, indent=2, default_flow_style=False)

    def repo_list(self):
        config = self._get_config_file()
        repos = config.get("repos", {})

        print(f" ** All repos **")

        if not repos:
            print(f"  No repos found")
            return 1

        for repo_name, repo_data in repos.items():
            print(f"")
            print(f" - {repo_name}")
            print(f"    URL: {repo_data.get('url')}")

            if "branch" in repo_data["revision"]:
                print(f"    Branch: {repo_data.get('revision', {}).get('branch', None)}")
            elif "tag" in repo_data["revision"]:
                print(f"    Tag: {repo_data.get('revision', {}).get('tag', None)}")
            else:
                raise SgitConfigException('No tag or "branch" key found inside "revision" block for repo "{name}')

    def repo_add(self, name, url, revision):
        if not name or not url or not revision:
            raise SgitConfigException(f'Name "{name}, url "{url}" or revision "{revision}" must be set')

        config = self._get_config_file()

        if name in config.get("repos", []):
            print(f'Repo with name "{name}" already exists in config file')
            return 1

        # TODO: It is bad that each repo will default to a branch type and not a tag type
        config["repos"][name] = {"url": url, "revision": {"branch": revision}}

        self._dump_config_file(config)

        print(f'Successfully added new repo "{name}"')

    def repo_set(self, name, attrib, value):
        if not attrib or not value:
            raise SgitConfigException(f'Attrib "{attrib}" or "{value}" must be set')

        config = self._get_config_file()

        if name not in config.get("repos", []):
            print(f'Repo with name "{name}" not found in config file')
            return 1

        if attrib == "tag":
            del config["repos"][name]["revision"]["tag"]
            config["repos"][name]["revision"]["tag"] = value
            print(f'Set tag for repo "{name}" to -> "{value}"')
        elif attrib == "branch":
            del config["repos"][name]["revision"]["branch"]
            config["repos"][name]["revision"]["branch"] = value
            print(f'Set branch for repo "{name}" to -> "{value}"')
        else:
            print(f"Unsupported set attribute operation")
            return 1

        self._dump_config_file(config)

    def yes_no(self, question):
        print(question)

        if self.answer_yes:
            print(f"INFO: Automatically answer yes to question")
            return True

        answer = input("(y/n) << ")

        return answer.lower().startswith("y")

    def fetch(self, repos):
        """
        Runs "git fetch" on one or more git repos.

        To update all enabled repos send in None as value.

        To update a subset of repo names, send in them as a list of strings.
        A empty list of items will update no repos.
        """
        print(f"DEBUG: Repo fetch input - {repos}")

        config = self._get_config_file()

        repos_to_fetch = []

        if repos is None:
            for repo_name in config["repos"]:
                repos_to_fetch.append(repo_name)

        if isinstance(repos, list):
            for repo_name in repos:
                if repo_name in config["repos"]:
                    repos_to_fetch.append(repo_name)
                else:
                    print(f"WARNING: repo '{repo_name}' not found in configuration")

        print(f"INFO: repos to fetch: {repos_to_fetch}")

        if len(repos_to_fetch) == 0:
            print(f"No repos to fetch found")
            return 1

        for repo_name in repos_to_fetch:
            try:
                repo_path = os.path.join(os.getcwd(), repo_name)
                git_repo = Repo(repo_path)

                print(f"Fetching git repo '{repo_name}'")
                fetch_results = git_repo.remotes.origin.fetch()
                print(f"Fetching completed for repo '{repo_name}'")

                for fetch_result in fetch_results:
                    print(f" - Fetch result: {fetch_result.name}")
            except git.exc.NoSuchPathError:
                print(f"Repo {repo_name} not found on disk. You must update to clone it before fetching")
                return 1

        print(f"Fetching for all repos completed")
        return 0

    def _get_active_repos(self, config):
        """
        Helper method that will return only the repos that is enabled and active for usage
        """
        active_repos = []

        for repo_name, repo_data in config.get("repos", {}).items():
            if repo_data.get("enable", True):
                active_repos.append(repo_name)

        return active_repos

    def update(self, names):
        """
        To update all repos defined in the configuration send in names=None

        To update a subset of repos send in a list of strings names=["repo1", "repo2"]

        Algorithm:
            - If the folder do not exists
                - clone the repo with Repo.clone_from
                - Update the rev to specified rev
            - If the folder do exists
                - If working_tree has any changes in it
                    - Throw error about working tree has changes
                - If working tree is empty
                    - Reset the repo to the specified rev
        """
        print(f"DEBUG: Repo update - {names}")

        config = self._get_config_file()

        active_repos = self._get_active_repos(config)

        repos = []

        if len(active_repos) == 0:
            print(f"ERROR: There is no repos defined or enabled in the config")
            return 1

        if names is None:
            repos = config.get("repos", [])
            repo_choices = ", ".join(active_repos)

            answer = self.yes_no(f'Are you sure you want to update the following repos "{repo_choices}"')

            if not answer:
                print(f"User aborted update step")
                return 1
        elif isinstance(names, list):
            # Validate that all provided repo names exists in the config
            for name in names:
                if name not in active_repos:
                    choices = ", ".join(active_repos)
                    print(f'Repo with name "{name}" not found in config file. Choices are "{choices}"')
                    return 1

            # If all repos was found, use the list of provided repos as list to process below
            repos = names
        else:
            print(f"DEBUG: names {names}")
            raise SgitConfigException(f"Unsuported value type for argument names")

        if not repos:
            raise SgitConfigException(f"No valid repositories found")

        #
        ## Validation step across all repos to manipulate that they are not dirty
        ## or anything uncommited that would break the code trees.
        ##
        ## Abort out if any repo is bad.
        #

        has_dirty = False

        for name in repos:
            repo_path = os.path.join(os.getcwd(), name)

            # If the path do not exists then the repo can't be dirty
            if not os.path.exists(repo_path):
                continue

            repo = Repo(repo_path)

            ## A dirty repo means there is uncommited changes in the tree
            if repo.is_dirty():
                print(f'ERROR: The repo "{name}" is dirty and has uncommited changes in the following files')
                dirty_files = [item.a_path for item in repo.index.diff(None)]

                for file in dirty_files:
                    print(f" - {file}")

                has_dirty = True

        if has_dirty:
            print(f"\nERROR: Found one or more dirty repos. Resolve it before continue...")
            return 1

        #
        ## Repos looks good to be updated. Run the update logic for each repo in sequence
        #

        for name in repos:
            repo_path = os.path.join(os.getcwd(), name)
            revision = config["repos"][name]["revision"]

            if not os.path.exists(repo_path):
                clone_rev = revision["tag"] if "tag" in revision else revision["branch"]

                try:
                    repo = Repo.clone_from(
                        config["repos"][name]["url"],
                        repo_path,
                        branch=clone_rev,
                    )
                    print(f'Successfully cloned repo "{name}" from remote server')
                except git.exc.GitCommandError as e:
                    # We assume that retcode 128 means you try to clone into a bare repo and we must
                    # attempt to clone it w/o a specific branch identifier.
                    if e.status == 128:
                        try:
                            repo = Repo.clone_from(
                                config["repos"][name]["url"],
                                repo_path,
                            )
                            print(f'Successfully cloned into bare git repo "{name}" from remote server')
                        except Exception as e:
                            raise SgitException(f'Clone into bare git repo "{name}" failed, exception: {e}')
                except Exception as e:
                    raise SgitException(f'Clone "{name}" failed, exception: {e}')
            else:
                print(f"TODO: Parse for any changes...")
                # TODO: Check that origin remote exists

                repo = Repo(os.path.join(os.getcwd(), name))

                g = Git(os.path.join(os.getcwd(), name))

                # Fetch all changes from upstream git repo
                repo.remotes.origin.fetch()

                # How to handle the repo when a branch is specified
                if "branch" in revision:
                    print(f"DEBUG: Handling branch update case")

                    # Extract the sub tag data
                    branch_revision = revision["branch"]

                    # Ensure the local version of the branch exists and points to the origin ref for that branch
                    repo.create_head(f"{branch_revision}", f"origin/{branch_revision}")

                    # Checkout the selected revision
                    # TODO: This only support branches for now
                    repo.heads[branch_revision].checkout()

                    print(f'Successfully update repo "{name}" to latest commit on branch "{branch_revision}"')
                    print(f"INFO: Current git hash on HEAD: {str(repo.head.commit)}")
                elif "tag" in revision:
                    #
                    # Parse and extract out all relevant config options and determine if they are nested
                    # dicts or single values. The values will later be used as input into each operation.
                    #
                    tag_config = revision["tag"]

                    # If "filter" key is not specified then we should not filter anything and keep all values
                    filter_config = tag_config.get("filter", [])

                    # If we do not have a list, convert it internally first
                    if isinstance(filter_config, str):
                        filter_config = [filter_config]

                    if not isinstance(filter_config, list):
                        raise SgitConfigException(f"filter option must be a list of items or a single string")

                    order_config = tag_config.get("order", None)
                    if order_config is None:
                        order_algorithm = OrderAlgorithms.SEMVER
                    else:
                        order_algorithm = OrderAlgorithms.__members__.get(order_config.upper(), None)

                        if order_algorithm is None:
                            raise SgitConfigException(f"Unsupported order algorithm chose: {order_config.upper()}")

                    select_config = tag_config.get("select", None)
                    select_method = None
                    if select_config is None:
                        raise SgitConfigException(f"select key is required in all tag revisions")

                    # We have sub options to extract out
                    if isinstance(select_config, dict):
                        select_config = select_config["value"]
                        select_method_value = select_config["method"]

                        select_method = SelectionMethods.__members__.get(select_method_value.upper(), None)

                        if select_method is None:
                            raise SgitConfigException(f"Unsupported select method chosen: {select_method_value.upper()}")
                    else:
                        select_method = SelectionMethods.SEMVER

                    print(f"DEBUG: {filter_config}")
                    print(f"DEBUG: {order_config}")
                    print(f"DEBUG: {order_algorithm}")
                    print(f"DEBUG: {select_config}")
                    print(f"DEBUG: {select_method}")

                    #
                    # Main tag parsing logic
                    #
                    git_repo_tags = [
                        str(tag)
                        for tag in repo.tags
                    ]
                    print(f"DEBUG: Raw git tags from git repo {git_repo_tags}")

                    filter_output = self._filter(git_repo_tags, filter_config)

                    # # FIXME: If we choose time as sorting method we must convert the data to a new format
                    # #        that the order algorithm allows.
                    # if order_algorithm == OrderAlgorithms.TIME:
                    #     pass

                    order_output = self._order(filter_output, order_algorithm)
                    select_output = self._select(order_output, select_config, select_method)
                    print(select_output)

                    if not select_output:
                        raise SgitRepoException(f"No git tag could be parsed out with the current repo configuration")

                    print(f"INFO: Attempting to checkout tag '{select_output}' for repo '{name}'")

                    # Otherwise atempt to checkout whatever we found. If our selection is still not something valid
                    # inside the git repo, we will get sub exceptions raised by git module.
                    g.checkout(select_output)

                    print(f"INFO: Checked out tag '{select_output}' for repo '{name}'")
                    print(f"INFO: Current git hash on HEAD: {str(repo.head.commit)}")
                    print(f"INFO: Current commit summary on HEAD: ")
                    print(f"INFO:     {str(repo.head.commit.summary)}")

    def _filter(self, sequence, regex_list):
        """
        Given a sequence of git objects, clean them against all regex items in the provided regex_list.

        Cleaning one item in the seuqence means that we can extract out any relevant information from our sequence
        in order to make further ordering and selection at later stages.

        The most basic example is to make semver comparisons we might need to remove prefixes and suffixes
        from the tag name in order to make a semver comparison.

        v1.0.0 would be cleaned to 1.0.0, and 1.1.0-beta1 would be cleaned to 1.1.0 and we can then make a semver
        comparison between them in order to find out the latest tag item.
        """
        filtered_sequence = []

        print(f"DEBUG: Running clean step on data")

        if not isinstance(regex_list, list):
            raise SgitConfigException(f"sequence for clean step must be a list of items")

        if not isinstance(regex_list, list):
            raise SgitConfigException(f"regex_list for clean step must be a list of items")

        # If we have no regex to filter against, then return original list unaltered
        if len(regex_list) == 0:
            return sequence

        for item in sequence:
            for filter_regex in regex_list:
                if not isinstance(filter_regex, str):
                    raise SgitConfigException(f"ERROR: filter regex must be a string")

                # A empty regex string is not valid
                if filter_regex.strip() == "":
                    raise SgitConfigException(f"ERROR: Empty regex filter string is not allowed")

                print(f"DEBUG: Filtering item '{item}' against regex '{filter_regex}")

                match_result = re.match(filter_regex, item)

                if match_result:
                    print(f"DEBUG: Filter match result hit: {match_result}")

                    # If the regex contains a group that is what we want to extract out and
                    # add to our filtered output list of results
                    if len(match_result.groups()) > 0:
                        filtered_sequence.append(match_result.groups()[0])
                    else:
                        filtered_sequence.append(item)

                    break

        print(f"DEBUG: Filter items result: {filtered_sequence}")

        return filtered_sequence

    def _order(self, sequence, method):
        """
        Given a sequence of git objects, order them based on what ordering algorithm selected.

        Some algorithms might require additional information in order to perform the ordering properly,
        in these cases each item in the sequence should be a tuple where the first value is the key or primary
        data we want to sort on, like tag name. But the second and/or third item in the tuple can be for example
        a timestamp or other metadata that we need to use within our algorithm to order them properly.

        Supports OrderAlgorithm methods: ALPHABETICAL, TIME, SEMVER

        Returns a new list with the sorted sequence of items
        """
        ordered_sequence = []

        if method == OrderAlgorithms.SEMVER:
            print(f"DEBUG: Ordering sequence of items by PEP440 SEMVER logic")
            print(sequence)

            ordered_sequence = list(
                sorted(
                    sequence,
                    key=lambda x: version.Version(x)
                )
            )
        elif method == OrderAlgorithms.TIME:
            # When sorting by time the latest item in the sequence with the highest or most recent time
            # will be on index[0] in the returned sequence.
            print(f"DEBUG: Ordering sequence of items by TIME they was created, input:")
            print(sequence)

            ordered_sequence = list(
                sorted(
                    sequence,
                    key=lambda t: t[1],
                )
            )
        elif method == OrderAlgorithms.ALPHABETICAL:
            print(f"DEBUG: Order sequence of items by ALPHABETICAL string order")
            print(sequence)

            # By default sorted will do alphabetical sort
            ordered_sequence = list(sorted(sequence))
        else:
            raise SgitConfigException(f"Unsupported ordering algorithm selected")

        print(f"DEBUG: Ordered sequence result: {ordered_sequence}")

        return ordered_sequence

    def _select(self, sequence, selection_query, selection_method):
        """
        Given a sequence of objects, perform the selection based on the selection_method and the
        logic that it implements.

        Supports: SEMVER, EXACT

        Defaults to SEMVER logic

        SEMVER: It will run you selection against the sequence of items and with a library supporting
                PEP440 semver comparison logic. Important note here is that it will take the highest
                version depending on the previous ordering that still fits the semver version check.

                Given a sequence of 1.1.0, 1.0.0, 0.9.0 and a selection of >= 1.0.0, it will select 1.1.0
                
                Given a sequence of 0.9.0, 1.0.0, 1.1.0 and a selection of >= 0.9.0, it will select 0.9.0
                as that item is first in the sequence that matches the query.

                Two special keywords exists, first and last. First will pick the first item in the sequence
                and last will pick the last item in the sequence. Combining this with different ordering logics
                we can get a bit more dynamic selection options.

        EXACT: This matching algorithm is more of a textual exact comparison that do not use any semver of
               comparison between items in the sequence. In the case you want to point to a specific commit
               that do not have any general semver information or data in it you should use this method.
        """
        if selection_method == SelectionMethods.SEMVER:
            if selection_query == "last":
                return sequence[-1]
            elif selection_query == "first":
                return sequence[0]
            else:
                spec = SpecifierSet(selection_query)

                filtered_versions = list(
                    spec.filter(
                        sequence,
                    )
                )

                print(f"DEBUG: filtered_versions")
                print(filtered_versions)

                return filtered_versions[-1]
        elif selection_method == SelectionMethods.EXACT:
            for item in sequence:
                if item == selection_query:
                    return item

            # Query not found in sequence, return None
            return None
        else:
            raise SgitConfigException(f"Unsupported select algorithm selected")
