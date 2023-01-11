from datetime import timedelta, datetime
import binascii
import filecmp
import sys
import hashlib
from io import BytesIO
import itertools
import math
import os
from pathlib import Path
from random import randrange
from subprocess import Popen
import re
import shutil
import traceback
import uuid
import ntplib
from lxml import etree
import pycdlib
import send2trash
from PyPDF2 import PdfFileMerger
from .GeneralUtilities import GeneralUtilities
from .ProgramRunnerBase import ProgramRunnerBase
from .ProgramRunnerPopen import ProgramRunnerPopen
from .ProgramRunnerEpew import ProgramRunnerEpew, CustomEpewArgument


version = "3.3.43"
__version__ = version


class ScriptCollectionCore:

    # The purpose of this property is to use it when testing your code which uses scriptcollection for external program-calls.
    # Do not change this value for productive environments.
    mock_program_calls: bool = False
    # The purpose of this property is to use it when testing your code which uses scriptcollection for external program-calls.
    execute_program_really_if_no_mock_call_is_defined: bool = False
    __mocked_program_calls: list = list()
    program_runner: ProgramRunnerBase = None

    def __init__(self):
        self.program_runner = ProgramRunnerPopen()

    @staticmethod
    @GeneralUtilities.check_arguments
    def get_scriptcollection_version() -> str:
        return __version__

    @GeneralUtilities.check_arguments
    def python_file_has_errors(self, file: str, working_directory: str, treat_warnings_as_errors: bool = True) -> tuple[bool, list[str]]:
        errors = list()
        filename = os.path.relpath(file, working_directory)
        if treat_warnings_as_errors:
            errorsonly_argument = ""
        else:
            errorsonly_argument = " --errors-only"
        (exit_code, stdout, stderr, _) = self.run_program("pylint", filename+errorsonly_argument, working_directory, throw_exception_if_exitcode_is_not_zero=False)
        if (exit_code != 0):
            errors.append(f"Linting-issues of {file}:")
            errors.append(f"Pylint-exitcode: {exit_code}")
            for line in GeneralUtilities.string_to_lines(stdout):
                errors.append(line)
            for line in GeneralUtilities.string_to_lines(stderr):
                errors.append(line)
            return (True, errors)

        return (False, errors)

    @GeneralUtilities.check_arguments
    def replace_version_in_dockerfile_file(self, dockerfile: str, new_version_value: str) -> None:
        GeneralUtilities.write_text_to_file(dockerfile, re.sub("ARG Version=\"\\d+\\.\\d+\\.\\d+\"", f"ARG Version=\"{new_version_value}\"",
                                                               GeneralUtilities.read_text_from_file(dockerfile)))

    @GeneralUtilities.check_arguments
    def check_testcoverage(self, testcoverage_file_in_cobertura_format: str, threshold_in_percent: float):
        root: etree._ElementTree = etree.parse(testcoverage_file_in_cobertura_format)
        coverage_in_percent = round(float(str(root.xpath('//coverage/@line-rate')[0]))*100, 2)
        minimalrequiredtestcoverageinpercent = threshold_in_percent
        if (coverage_in_percent < minimalrequiredtestcoverageinpercent):
            raise ValueError(f"The testcoverage must be {minimalrequiredtestcoverageinpercent}% or more but is {coverage_in_percent}%.")

    @GeneralUtilities.check_arguments
    def replace_version_in_python_file(self, file: str, new_version_value: str):
        GeneralUtilities.write_text_to_file(file, re.sub("version = \"\\d+\\.\\d+\\.\\d+\"", f"version = \"{new_version_value}\"",
                                                         GeneralUtilities.read_text_from_file(file)))

    @GeneralUtilities.check_arguments
    def replace_version_in_ini_file(self, file: str, new_version_value: str):
        GeneralUtilities.write_text_to_file(file, re.sub("version = \\d+\\.\\d+\\.\\d+", f"version = {new_version_value}",
                                                         GeneralUtilities.read_text_from_file(file)))

    @GeneralUtilities.check_arguments
    def replace_version_in_nuspec_file(self, nuspec_file: str, new_version: str) -> None:
        # TODO use XSLT instead
        versionregex = "\\d+\\.\\d+\\.\\d+"
        versiononlyregex = f"^{versionregex}$"
        pattern = re.compile(versiononlyregex)
        if pattern.match(new_version):
            GeneralUtilities.write_text_to_file(nuspec_file, re.sub(f"<version>{versionregex}<\\/version>",
                                                                    f"<version>{new_version}</version>", GeneralUtilities.read_text_from_file(nuspec_file)))
        else:
            raise ValueError(f"Version '{new_version}' does not match version-regex '{versiononlyregex}'")

    @GeneralUtilities.check_arguments
    def replace_version_in_csproj_file(self, csproj_file: str, current_version: str):
        versionregex = "\\d+\\.\\d+\\.\\d+"
        versiononlyregex = f"^{versionregex}$"
        pattern = re.compile(versiononlyregex)
        if pattern.match(current_version):
            for tag in ["Version", "AssemblyVersion", "FileVersion"]:
                GeneralUtilities.write_text_to_file(csproj_file, re.sub(f"<{tag}>{versionregex}(.\\d+)?<\\/{tag}>",
                                                                        f"<{tag}>{current_version}</{tag}>", GeneralUtilities.read_text_from_file(csproj_file)))
        else:
            raise ValueError(f"Version '{current_version}' does not match version-regex '{versiononlyregex}'")

    @GeneralUtilities.check_arguments
    def push_nuget_build_artifact(self, nupkg_file: str, registry_address: str, api_key: str, verbosity: int = 1):
        nupkg_file_name = os.path.basename(nupkg_file)
        nupkg_file_folder = os.path.dirname(nupkg_file)
        self.run_program("dotnet", f"nuget push {nupkg_file_name} --force-english-output --source {registry_address} --api-key {api_key}",
                         nupkg_file_folder, verbosity)

    @GeneralUtilities.check_arguments
    def dotnet_build(self, repository_folder: str, projectname: str, configuration: str):
        self.run_program("dotnet", f"clean -c {configuration}", repository_folder)
        self.run_program("dotnet", f"build {projectname}/{projectname}.csproj -c {configuration}", repository_folder)

    @GeneralUtilities.check_arguments
    def dotnet_sign(self, dllOrExefile: str, snkfile: str, verbosity: int, current_release_information: dict[str, str]) -> None:
        dllOrExeFile = GeneralUtilities.resolve_relative_path_from_current_working_directory(dllOrExefile)
        snkfile = GeneralUtilities.resolve_relative_path_from_current_working_directory(snkfile)
        directory = os.path.dirname(dllOrExeFile)
        filename = os.path.basename(dllOrExeFile)
        if filename.lower().endswith(".dll"):
            filename = filename[:-4]
            extension = "dll"
        elif filename.lower().endswith(".exe"):
            filename = filename[:-4]
            extension = "exe"
        else:
            raise Exception("Only .dll-files and .exe-files can be signed")
        self.run_program("ildasm",
                         f'/all /typelist /text /out="{filename}.il" "{filename}.{extension}"',
                         directory,  verbosity, False, "Sign: ildasm")
        self.run_program("ilasm",
                         f'/{extension} /res:"{filename}.res" /optimize /key="{snkfile}" "{filename}.il"',
                         directory,  verbosity, False, "Sign: ilasm")
        os.remove(directory+os.path.sep+filename+".il")
        os.remove(directory+os.path.sep+filename+".res")

    @GeneralUtilities.check_arguments
    def find_file_by_extension(self, folder: str, extension: str):
        result = [file for file in GeneralUtilities.get_direct_files_of_folder(folder) if file.endswith(f".{extension}")]
        result_length = len(result)
        if result_length == 0:
            raise FileNotFoundError(f"No file available in folder '{folder}' with extension '{extension}'.")
        if result_length == 1:
            return result[0]
        else:
            raise ValueError(f"Multiple values available in folder '{folder}' with extension '{extension}'.")

    @GeneralUtilities.check_arguments
    def dotnet_sign_file(self, file: str, keyfile: str, verbosity: int):
        directory = os.path.dirname(file)
        filename = os.path.basename(file)
        if filename.lower().endswith(".dll"):
            filename = filename[:-4]
            extension = "dll"
        elif filename.lower().endswith(".exe"):
            filename = filename[:-4]
            extension = "exe"
        else:
            raise Exception("Only .dll-files and .exe-files can be signed")
        self.run_program("ildasm", f'/all /typelist /text /out={filename}.il {filename}.{extension}', directory, verbosity=verbosity)
        self.run_program("ilasm", f'/{extension} /res:{filename}.res /optimize /key={keyfile} {filename}.il', directory, verbosity=verbosity)
        os.remove(directory+os.path.sep+filename+".il")
        os.remove(directory+os.path.sep+filename+".res")

    @GeneralUtilities.check_arguments
    def commit_is_signed_by_key(self, repository_folder: str, revision_identifier: str, key: str) -> bool:
        result = self.run_program("git", f"verify-commit {revision_identifier}", repository_folder, throw_exception_if_exitcode_is_not_zero=False)
        if (result[0] != 0):
            return False
        if (not GeneralUtilities.contains_line(result[1].splitlines(), f"gpg\\:\\ using\\ [A-Za-z0-9]+\\ key\\ [A-Za-z0-9]+{key}")):
            # TODO check whether this works on machines where gpg is installed in another langauge than english
            return False
        if (not GeneralUtilities.contains_line(result[1].splitlines(), "gpg\\:\\ Good\\ signature\\ from")):
            # TODO check whether this works on machines where gpg is installed in another langauge than english
            return False
        return True

    @GeneralUtilities.check_arguments
    def get_parent_commit_ids_of_commit(self, repository_folder: str, commit_id: str) -> str:
        return self.run_program("git", f'log --pretty=%P -n 1 "{commit_id}"',
                                       repository_folder, throw_exception_if_exitcode_is_not_zero=True)[1].replace("\r", "").replace("\n", "").split(" ")

    @GeneralUtilities.check_arguments
    def get_commit_ids_between_dates(self, repository_folder: str, since: datetime, until: datetime, ignore_commits_which_are_not_in_history_of_head: bool = True) -> None:
        since_as_string = self.__datetime_to_string_for_git(since)
        until_as_string = self.__datetime_to_string_for_git(until)
        result = filter(lambda line: not GeneralUtilities.string_is_none_or_whitespace(line),
                        self.run_program("git", f'log --since "{since_as_string}" --until "{until_as_string}" --pretty=format:"%H" --no-patch',
                                         repository_folder, throw_exception_if_exitcode_is_not_zero=True)[1].split("\n").replace("\r", ""))
        if ignore_commits_which_are_not_in_history_of_head:
            result = [commit_id for commit_id in result if self.git_commit_is_ancestor(repository_folder, commit_id)]
        return result

    @GeneralUtilities.check_arguments
    def __datetime_to_string_for_git(self, datetime_object: datetime) -> str:
        return datetime_object.strftime('%Y-%m-%d %H:%M:%S')

    @GeneralUtilities.check_arguments
    def git_commit_is_ancestor(self, repository_folder: str,  ancestor: str, descendant: str = "HEAD") -> bool:
        return self.run_program_argsasarray("git", ["merge-base", "--is-ancestor", ancestor, descendant], repository_folder, throw_exception_if_exitcode_is_not_zero=False)[0] == 0

    @GeneralUtilities.check_arguments
    def __git_changes_helper(self, repository_folder: str, arguments_as_array: list[str]) -> bool:
        lines = GeneralUtilities.string_to_lines(self.run_program_argsasarray("git", arguments_as_array, repository_folder,
                                                 throw_exception_if_exitcode_is_not_zero=True, verbosity=0)[1], False)
        for line in lines:
            if GeneralUtilities.string_has_content(line):
                return True
        return False

    @GeneralUtilities.check_arguments
    def git_repository_has_new_untracked_files(self, repositoryFolder: str):
        return self.__git_changes_helper(repositoryFolder, ["ls-files", "--exclude-standard", "--others"])

    @GeneralUtilities.check_arguments
    def git_repository_has_unstaged_changes_of_tracked_files(self, repositoryFolder: str):
        return self.__git_changes_helper(repositoryFolder, ["diff"])

    @GeneralUtilities.check_arguments
    def git_repository_has_staged_changes(self, repositoryFolder: str):
        return self.__git_changes_helper(repositoryFolder, ["diff", "--cached"])

    @GeneralUtilities.check_arguments
    def git_repository_has_uncommitted_changes(self, repositoryFolder: str) -> bool:
        if (self.git_repository_has_unstaged_changes(repositoryFolder)):
            return True
        if (self.git_repository_has_staged_changes(repositoryFolder)):
            return True
        return False

    @GeneralUtilities.check_arguments
    def git_repository_has_unstaged_changes(self, repository_folder: str) -> bool:
        if (self.git_repository_has_unstaged_changes_of_tracked_files(repository_folder)):
            return True
        if (self.git_repository_has_new_untracked_files(repository_folder)):
            return True
        return False

    @GeneralUtilities.check_arguments
    def git_get_commit_id(self, repository_folder: str, commit: str = "HEAD") -> str:
        result: tuple[int, str, str, int] = self.run_program_argsasarray("git", ["rev-parse", "--verify", commit],
                                                                         repository_folder, throw_exception_if_exitcode_is_not_zero=True, verbosity=0)
        return result[1].replace('\n', '')

    @GeneralUtilities.check_arguments
    def git_get_commit_date(self, repository_folder: str, commit: str = "HEAD") -> datetime:
        result: tuple[int, str, str, int] = self.run_program_argsasarray("git", ["show", "-s", "--format=%ci", commit],
                                                                         repository_folder, throw_exception_if_exitcode_is_not_zero=True, verbosity=0)
        date_as_string = result[1].replace('\n', '')
        result = datetime.strptime(date_as_string, '%Y-%m-%d %H:%M:%S %z')
        return result

    @GeneralUtilities.check_arguments
    def git_fetch(self, folder: str, remotename: str = "--all") -> None:
        self.run_program_argsasarray("git", ["fetch", remotename, "--tags", "--prune"], folder, throw_exception_if_exitcode_is_not_zero=True, verbosity=0)

    @GeneralUtilities.check_arguments
    def git_fetch_in_bare_repository(self, folder: str, remotename, localbranch: str, remotebranch: str) -> None:
        self.run_program_argsasarray("git", ["fetch", remotename, f"{remotebranch}:{localbranch}"], folder, throw_exception_if_exitcode_is_not_zero=True, verbosity=0)

    @GeneralUtilities.check_arguments
    def git_remove_branch(self, folder: str, branchname: str) -> None:
        self.run_program("git", f"branch -D {branchname}", folder, throw_exception_if_exitcode_is_not_zero=True, verbosity=0)

    @GeneralUtilities.check_arguments
    def git_push(self, folder: str, remotename: str, localbranchname: str, remotebranchname: str, forcepush: bool = False, pushalltags: bool = True, verbosity: int = 0) -> None:
        argument = ["push", "--recurse-submodules=on-demand", remotename, f"{localbranchname}:{remotebranchname}"]
        if (forcepush):
            argument.append("--force")
        if (pushalltags):
            argument.append("--tags")
        result: tuple[int, str, str, int] = self.run_program_argsasarray("git", argument, folder, throw_exception_if_exitcode_is_not_zero=True,
                                                                         verbosity=verbosity, print_errors_as_information=True)
        return result[1].replace('\r', '').replace('\n', '')

    @GeneralUtilities.check_arguments
    def git_clone(self, clone_target_folder: str, remote_repository_path: str, include_submodules: bool = True, mirror: bool = False) -> None:
        if (os.path.isdir(clone_target_folder)):
            pass  # TODO throw error
        else:
            args = ["clone", remote_repository_path, clone_target_folder]
            if include_submodules:
                args.append("--recurse-submodules")
                args.append("--remote-submodules")
            if mirror:
                args.append("--mirror")
            self.run_program_argsasarray("git", args, os.getcwd(), throw_exception_if_exitcode_is_not_zero=True, verbosity=0)

    @GeneralUtilities.check_arguments
    def git_get_all_remote_names(self, directory) -> list[str]:
        result = GeneralUtilities.string_to_lines(self.run_program_argsasarray("git", ["remote"], directory, throw_exception_if_exitcode_is_not_zero=True, verbosity=0)[1], False)
        return result

    @GeneralUtilities.check_arguments
    def repository_has_remote_with_specific_name(self, directory: str, remote_name: str) -> bool:
        return remote_name in self.git_get_all_remote_names(directory)

    @GeneralUtilities.check_arguments
    def git_add_or_set_remote_address(self, directory: str, remote_name: str, remote_address: str) -> None:
        if (self.repository_has_remote_with_specific_name(directory, remote_name)):
            self.run_program_argsasarray("git", ['remote', 'set-url', 'remote_name', remote_address], directory, throw_exception_if_exitcode_is_not_zero=True, verbosity=0)
        else:
            self.run_program_argsasarray("git", ['remote', 'add', remote_name, remote_address], directory, throw_exception_if_exitcode_is_not_zero=True, verbosity=0)

    @GeneralUtilities.check_arguments
    def git_stage_all_changes(self, directory: str) -> None:
        self.run_program_argsasarray("git", ["add", "-A"], directory, throw_exception_if_exitcode_is_not_zero=True, verbosity=0)

    @GeneralUtilities.check_arguments
    def git_unstage_all_changes(self, directory: str) -> None:
        self.run_program_argsasarray("git", ["reset"], directory, throw_exception_if_exitcode_is_not_zero=True, verbosity=0)

    @GeneralUtilities.check_arguments
    def git_stage_file(self, directory: str, file: str) -> None:
        self.run_program_argsasarray("git", ['stage', file], directory, throw_exception_if_exitcode_is_not_zero=True, verbosity=0)

    @GeneralUtilities.check_arguments
    def git_unstage_file(self, directory: str, file: str) -> None:
        self.run_program_argsasarray("git", ['reset', file], directory, throw_exception_if_exitcode_is_not_zero=True, verbosity=0)

    @GeneralUtilities.check_arguments
    def git_discard_unstaged_changes_of_file(self, directory: str, file: str) -> None:
        """Caution: This method works really only for 'changed' files yet. So this method does not work properly for new or renamed files."""
        self.run_program_argsasarray("git", ['checkout', file], directory, throw_exception_if_exitcode_is_not_zero=True, verbosity=0)

    @GeneralUtilities.check_arguments
    def git_discard_all_unstaged_changes(self, directory: str) -> None:
        """Caution: This function executes 'git clean -df'. This can delete files which maybe should not be deleted. Be aware of that."""
        self.run_program_argsasarray("git", ['clean', '-df'], directory, throw_exception_if_exitcode_is_not_zero=True, verbosity=0)
        self.run_program_argsasarray("git", ['checkout', '.'], directory, throw_exception_if_exitcode_is_not_zero=True, verbosity=0)

    @GeneralUtilities.check_arguments
    def git_commit(self, directory: str, message: str, author_name: str = None, author_email: str = None, stage_all_changes: bool = True,
                   no_changes_behavior: int = 0) -> str:
        # no_changes_behavior=0 => No commit
        # no_changes_behavior=1 => Commit anyway
        # no_changes_behavior=2 => Exception
        author_name = GeneralUtilities.str_none_safe(author_name).strip()
        author_email = GeneralUtilities.str_none_safe(author_email).strip()
        argument = ['commit', '--quiet', '--message', message]
        if (GeneralUtilities.string_has_content(author_name)):
            argument.append(f'--author="{author_name} <{author_email}>"')
        git_repository_has_uncommitted_changes = self.git_repository_has_uncommitted_changes(directory)

        if git_repository_has_uncommitted_changes:
            do_commit = True
            if stage_all_changes:
                self.git_stage_all_changes(directory)
        else:
            if no_changes_behavior == 0:
                GeneralUtilities.write_message_to_stdout(f"Commit '{message}' will not be done because there are no changes to commit in repository '{directory}'")
                do_commit = False
            if no_changes_behavior == 1:
                GeneralUtilities.write_message_to_stdout(f"There are no changes to commit in repository '{directory}'. Commit '{message}' will be done anyway.")
                do_commit = True
                argument.append('--allow-empty')
            if no_changes_behavior == 2:
                raise RuntimeError(f"There are no changes to commit in repository '{directory}'. Commit '{message}' will not be done.")

        if do_commit:
            GeneralUtilities.write_message_to_stdout(f"Commit changes in '{directory}'")
            self.run_program_argsasarray("git", argument, directory, throw_exception_if_exitcode_is_not_zero=True, verbosity=0)

        return self.git_get_commit_id(directory)

    @GeneralUtilities.check_arguments
    def git_create_tag(self, directory: str, target_for_tag: str, tag: str, sign: bool = False, message: str = None) -> None:
        argument = ["tag", tag, target_for_tag]
        if sign:
            if message is None:
                message = f"Created {target_for_tag}"
            argument.extend(["-s", '-m', message])
        self.run_program_argsasarray("git", argument, directory, throw_exception_if_exitcode_is_not_zero=True, verbosity=0)

    @GeneralUtilities.check_arguments
    def git_checkout(self, directory: str, branch: str) -> None:
        self.run_program_argsasarray("git", ["checkout", branch], directory, throw_exception_if_exitcode_is_not_zero=True, verbosity=0)

    @GeneralUtilities.check_arguments
    def git_merge_abort(self, directory: str) -> None:
        self.run_program_argsasarray("git", ["merge", "--abort"], directory, throw_exception_if_exitcode_is_not_zero=True, verbosity=0)

    @GeneralUtilities.check_arguments
    def git_merge(self, directory: str, sourcebranch: str, targetbranch: str, fastforward: bool = True, commit: bool = True, commit_message: str = None) -> str:
        self.git_checkout(directory, targetbranch)
        args = ["merge"]
        if not commit:
            args.append("--no-commit")
        if not fastforward:
            args.append("--no-ff")
        if commit_message is not None:
            args.append("-m")
            args.append(commit_message)
        args.append(sourcebranch)
        self.run_program_argsasarray("git", args, directory, throw_exception_if_exitcode_is_not_zero=True, verbosity=0)
        return self.git_get_commit_id(directory)

    @GeneralUtilities.check_arguments
    def git_undo_all_changes(self, directory: str) -> None:
        """Caution: This function executes 'git clean -df'. This can delete files which maybe should not be deleted. Be aware of that."""
        self.git_unstage_all_changes(directory)
        self.git_discard_all_unstaged_changes(directory)

    @GeneralUtilities.check_arguments
    def git_fetch_or_clone_all_in_directory(self, source_directory: str, target_directory: str) -> None:
        for subfolder in GeneralUtilities.get_direct_folders_of_folder(source_directory):
            foldername = os.path.basename(subfolder)
            if self.is_git_repository(subfolder):
                source_repository = subfolder
                target_repository = os.path.join(target_directory, foldername)
                if os.path.isdir(target_directory):
                    # fetch
                    self.git_fetch(target_directory)
                else:
                    # clone
                    self.git_clone(target_repository, source_repository, include_submodules=True, mirror=True)

    @GeneralUtilities.check_arguments
    def is_git_repository(self, folder: str) -> bool:
        combined = os.path.join(folder, ".git")
        # TODO consider check for bare-repositories
        return os.path.isdir(combined) or os.path.isfile(combined)

    @GeneralUtilities.check_arguments
    def file_is_git_ignored(self, file_in_repository: str, repositorybasefolder: str) -> None:
        exit_code = self.run_program_argsasarray("git", ['check-ignore', file_in_repository], repositorybasefolder, throw_exception_if_exitcode_is_not_zero=False, verbosity=0)[0]
        if (exit_code == 0):
            return True
        if (exit_code == 1):
            return False
        raise Exception(f"Unable to calculate whether '{file_in_repository}' in repository '{repositorybasefolder}' is ignored due to git-exitcode {exit_code}.")

    @GeneralUtilities.check_arguments
    def discard_all_changes(self, repository: str) -> None:
        self.run_program_argsasarray("git", ["reset", "HEAD", "."], repository, throw_exception_if_exitcode_is_not_zero=True, verbosity=0)
        self.run_program_argsasarray("git", ["checkout", "."], repository, throw_exception_if_exitcode_is_not_zero=True, verbosity=0)

    @GeneralUtilities.check_arguments
    def git_get_current_branch_name(self, repository: str) -> str:
        result = self.run_program_argsasarray("git", ["rev-parse", "--abbrev-ref", "HEAD"], repository, throw_exception_if_exitcode_is_not_zero=True, verbosity=0)
        return result[1].replace("\r", "").replace("\n", "")

    @GeneralUtilities.check_arguments
    def export_filemetadata(self, folder: str, target_file: str, encoding: str = "utf-8", filter_function=None) -> None:
        folder = GeneralUtilities.resolve_relative_path_from_current_working_directory(folder)
        lines = list()
        path_prefix = len(folder)+1
        items = dict()
        for item in GeneralUtilities.get_all_folders_of_folder(folder):
            items[item] = "d"
        for item in GeneralUtilities.get_all_files_of_folder(folder):
            items[item] = "f"
        for file_or_folder, item_type in items.items():
            truncated_file = file_or_folder[path_prefix:]
            if (filter_function is None or filter_function(folder, truncated_file)):
                owner_and_permisssion = self.get_file_owner_and_file_permission(file_or_folder)
                user = owner_and_permisssion[0]
                permissions = owner_and_permisssion[1]
                lines.append(f"{truncated_file};{item_type};{user};{permissions}")
        lines = sorted(lines, key=str.casefold)
        with open(target_file, "w", encoding=encoding) as file_object:
            file_object.write("\n".join(lines))

    def escape_git_repositories_in_folder(self, folder: str) -> dict[str, str]:
        return self.__escape_git_repositories_in_folder_internal(folder, dict[str, str]())

    def __escape_git_repositories_in_folder_internal(self, folder: str, renamed_items: dict[str, str]) -> dict[str, str]:
        for file in GeneralUtilities.get_direct_files_of_folder(folder):
            filename = os.path.basename(file)
            if ".git" in filename:
                new_name = filename.replace(".git", ".gitx")
                target = os.path.join(folder, new_name)
                os.rename(file, target)
                renamed_items[target] = file
        for subfolder in GeneralUtilities.get_direct_folders_of_folder(folder):
            foldername = os.path.basename(subfolder)
            if ".git" in foldername:
                new_name = foldername.replace(".git", ".gitx")
                subfolder2 = os.path.join(str(Path(subfolder).parent), new_name)
                os.rename(subfolder, subfolder2)
                renamed_items[subfolder2] = subfolder
            else:
                subfolder2 = subfolder
            self.__escape_git_repositories_in_folder_internal(subfolder2, renamed_items)
        return renamed_items

    def deescape_git_repositories_in_folder(self, renamed_items: dict[str, str]):
        for renamed_item, original_name in renamed_items.items():
            os.rename(renamed_item, original_name)

    def __sort_fmd(self, line: str):
        splitted: list = line.split(";")
        filetype: str = splitted[1]
        if filetype == "d":
            return -1
        if filetype == "f":
            return 1
        return 0

    @GeneralUtilities.check_arguments
    def restore_filemetadata(self, folder: str, source_file: str, strict=False, encoding: str = "utf-8", create_folder_is_not_exist: bool = True) -> None:
        lines = GeneralUtilities.read_lines_from_file(source_file, encoding)
        lines.sort(key=self.__sort_fmd)
        for line in lines:
            splitted: list = line.split(";")
            full_path_of_file_or_folder: str = os.path.join(folder, splitted[0])
            filetype: str = splitted[1]
            user: str = splitted[2]
            permissions: str = splitted[3]
            if filetype == "d" and create_folder_is_not_exist and not os.path.isdir(full_path_of_file_or_folder):
                GeneralUtilities.ensure_directory_exists(full_path_of_file_or_folder)
            if (filetype == "f" and os.path.isfile(full_path_of_file_or_folder)) or (filetype == "d" and os.path.isdir(full_path_of_file_or_folder)):
                self.set_owner(full_path_of_file_or_folder, user, os.name != 'nt')
                self.set_permission(full_path_of_file_or_folder, permissions)
            else:
                if strict:
                    if filetype == "f":
                        filetype_full = "File"
                    if filetype == "d":
                        filetype_full = "Directory"
                    raise Exception(f"{filetype_full} '{full_path_of_file_or_folder}' does not exist")

    @GeneralUtilities.check_arguments
    def __calculate_lengh_in_seconds(self, filename: str, folder: str) -> float:
        argument = ['-v', 'error', '-show_entries', 'format=duration', '-of', 'default=noprint_wrappers=1:nokey=1', filename]
        result = self.run_program_argsasarray("ffprobe", argument, folder, throw_exception_if_exitcode_is_not_zero=True)
        return float(result[1].replace('\n', ''))

    @GeneralUtilities.check_arguments
    def __create_thumbnails(self, filename: str, fps: str, folder: str, tempname_for_thumbnails: str) -> None:
        argument = ['-i', filename, '-r', str(fps), '-vf', 'scale=-1:120', '-vcodec', 'png', f'{tempname_for_thumbnails}-%002d.png']
        self.run_program_argsasarray("ffmpeg", argument, folder, throw_exception_if_exitcode_is_not_zero=True)

    @GeneralUtilities.check_arguments
    def __create_thumbnail(self, outputfilename: str, folder: str, length_in_seconds: float, tempname_for_thumbnails: str, amount_of_images: int) -> None:
        duration = timedelta(seconds=length_in_seconds)
        info = GeneralUtilities.timedelta_to_simple_string(duration)
        next_square_number = str(int(math.sqrt(GeneralUtilities.get_next_square_number(amount_of_images))))
        argument = ['-title', f'"{outputfilename} ({info})"', '-tile', f'{next_square_number}x{next_square_number}',
                    f'{tempname_for_thumbnails}*.png', f'{outputfilename}.png']
        self.run_program_argsasarray("montage", argument, folder, throw_exception_if_exitcode_is_not_zero=True)

    @GeneralUtilities.check_arguments
    def roundup(self, x: float, places: int) -> int:
        d = 10 ** places
        if x < 0:
            return math.floor(x * d) / d
        else:
            return math.ceil(x * d) / d

    @GeneralUtilities.check_arguments
    def generate_thumbnail(self, file: str, frames_per_second: str, tempname_for_thumbnails: str = None) -> None:
        if tempname_for_thumbnails is None:
            tempname_for_thumbnails = "t"+str(uuid.uuid4())

        file = GeneralUtilities.resolve_relative_path_from_current_working_directory(file)
        filename = os.path.basename(file)
        folder = os.path.dirname(file)
        filename_without_extension = Path(file).stem

        try:
            length_in_seconds = self.__calculate_lengh_in_seconds(filename, folder)
            if (frames_per_second.endswith("fps")):
                # frames per second, example: frames_per_second="20fps" => 20 frames per second
                x = self.roundup(float(frames_per_second[:-3]), 2)
                frames_per_secondx = str(x)
                amounf_of_previewframes = int(math.floor(length_in_seconds*x))
            else:
                # concrete amount of frame, examples: frames_per_second="16" => 16 frames for entire video
                amounf_of_previewframes = int(float(frames_per_second))
                frames_per_secondx = f"{amounf_of_previewframes-2}/{length_in_seconds}"  # self.roundup((amounf_of_previewframes-2)/length_in_seconds, 2)
            self.__create_thumbnails(filename, frames_per_secondx, folder, tempname_for_thumbnails)
            self.__create_thumbnail(filename_without_extension, folder, length_in_seconds, tempname_for_thumbnails, amounf_of_previewframes)
        finally:
            for thumbnail_to_delete in Path(folder).rglob(tempname_for_thumbnails+"-*"):
                file = str(thumbnail_to_delete)
                os.remove(file)

    @GeneralUtilities.check_arguments
    def merge_pdf_files(self, files, outputfile: str) -> None:
        # TODO add wildcard-option
        pdfFileMerger = PdfFileMerger()
        for file in files:
            pdfFileMerger.append(file.strip())
        pdfFileMerger.write(outputfile)
        pdfFileMerger.close()
        return 0

    @GeneralUtilities.check_arguments
    def SCShowMissingFiles(self, folderA: str, folderB: str):
        for file in GeneralUtilities.get_missing_files(folderA, folderB):
            GeneralUtilities.write_message_to_stdout(file)

    @GeneralUtilities.check_arguments
    def SCCreateEmptyFileWithSpecificSize(self, name: str, size_string: str) -> int:
        if size_string.isdigit():
            size = int(size_string)
        else:
            if len(size_string) >= 3:
                if (size_string.endswith("kb")):
                    size = int(size_string[:-2]) * pow(10, 3)
                elif (size_string.endswith("mb")):
                    size = int(size_string[:-2]) * pow(10, 6)
                elif (size_string.endswith("gb")):
                    size = int(size_string[:-2]) * pow(10, 9)
                elif (size_string.endswith("kib")):
                    size = int(size_string[:-3]) * pow(2, 10)
                elif (size_string.endswith("mib")):
                    size = int(size_string[:-3]) * pow(2, 20)
                elif (size_string.endswith("gib")):
                    size = int(size_string[:-3]) * pow(2, 30)
                else:
                    GeneralUtilities.write_message_to_stderr("Wrong format")
            else:
                GeneralUtilities.write_message_to_stderr("Wrong format")
                return 1
        with open(name, "wb") as f:
            f.seek(size-1)
            f.write(b"\0")
        return 0

    @GeneralUtilities.check_arguments
    def SCCreateHashOfAllFiles(self, folder: str) -> None:
        for file in GeneralUtilities.absolute_file_paths(folder):
            with open(file+".sha256", "w+", encoding="utf-8") as f:
                f.write(GeneralUtilities.get_sha256_of_file(file))

    @GeneralUtilities.check_arguments
    def SCCreateSimpleMergeWithoutRelease(self, repository: str, sourcebranch: str, targetbranch: str, remotename: str, remove_source_branch: bool) -> None:
        commitid = self.git_merge(repository, sourcebranch, targetbranch, False, True)
        self.git_merge(repository, targetbranch, sourcebranch, True, True)
        created_version = self.get_semver_version_from_gitversion(repository)
        self.git_create_tag(repository, commitid, f"v{created_version}", True)
        self.git_push(repository, remotename, targetbranch, targetbranch, False, True)
        if (GeneralUtilities.string_has_nonwhitespace_content(remotename)):
            self.git_push(repository, remotename, sourcebranch, sourcebranch, False, True)
        if (remove_source_branch):
            self.git_remove_branch(repository, sourcebranch)

    @GeneralUtilities.check_arguments
    def sc_organize_lines_in_file(self, file: str, encoding: str, sort: bool = False, remove_duplicated_lines: bool = False, ignore_first_line: bool = False,
                                  remove_empty_lines: bool = True, ignored_start_character: list = list()) -> int:
        if os.path.isfile(file):

            # read file
            lines = GeneralUtilities.read_lines_from_file(file, encoding)
            if (len(lines) == 0):
                return 0

            # store first line if desiredpopd

            if (ignore_first_line):
                first_line = lines.pop(0)

            # remove empty lines if desired
            if remove_empty_lines:
                temp = lines
                lines = []
                for line in temp:
                    if (not (GeneralUtilities.string_is_none_or_whitespace(line))):
                        lines.append(line)

            # remove duplicated lines if desired
            if remove_duplicated_lines:
                lines = GeneralUtilities.remove_duplicates(lines)

            # sort lines if desired
            if sort:
                lines = sorted(lines, key=lambda singleline: self.__adapt_line_for_sorting(singleline, ignored_start_character))

            # reinsert first line
            if ignore_first_line:
                lines.insert(0, first_line)

            # write result to file
            GeneralUtilities.write_lines_to_file(file, lines, encoding)

            return 0
        else:
            GeneralUtilities.write_message_to_stdout(f"File '{file}' does not exist")
            return 1

    @GeneralUtilities.check_arguments
    def __adapt_line_for_sorting(self, line: str, ignored_start_characters: list):
        result = line.lower()
        while len(result) > 0 and result[0] in ignored_start_characters:
            result = result[1:]
        return result

    @GeneralUtilities.check_arguments
    def SCGenerateSnkFiles(self, outputfolder, keysize=4096, amountofkeys=10) -> int:
        GeneralUtilities.ensure_directory_exists(outputfolder)
        for _ in range(amountofkeys):
            file = os.path.join(outputfolder, str(uuid.uuid4())+".snk")
            argument = f"-k {keysize} {file}"
            self.run_program("sn", argument, outputfolder)

    @GeneralUtilities.check_arguments
    def __merge_files(self, sourcefile: str, targetfile: str) -> None:
        with open(sourcefile, "rb") as f:
            source_data = f.read()
        with open(targetfile, "ab") as fout:
            merge_separator = [0x0A]
            fout.write(bytes(merge_separator))
            fout.write(source_data)

    @GeneralUtilities.check_arguments
    def __process_file(self, file: str, substringInFilename: str, newSubstringInFilename: str, conflictResolveMode: str) -> None:
        new_filename = os.path.join(os.path.dirname(file), os.path.basename(file).replace(substringInFilename, newSubstringInFilename))
        if file != new_filename:
            if os.path.isfile(new_filename):
                if filecmp.cmp(file, new_filename):
                    send2trash.send2trash(file)
                else:
                    if conflictResolveMode == "ignore":
                        pass
                    elif conflictResolveMode == "preservenewest":
                        if (os.path.getmtime(file) - os.path.getmtime(new_filename) > 0):
                            send2trash.send2trash(file)
                        else:
                            send2trash.send2trash(new_filename)
                            os.rename(file, new_filename)
                    elif (conflictResolveMode == "merge"):
                        self.__merge_files(file, new_filename)
                        send2trash.send2trash(file)
                    else:
                        raise Exception('Unknown conflict resolve mode')
            else:
                os.rename(file, new_filename)

    @GeneralUtilities.check_arguments
    def SCReplaceSubstringsInFilenames(self, folder: str, substringInFilename: str, newSubstringInFilename: str, conflictResolveMode: str) -> None:
        for file in GeneralUtilities.absolute_file_paths(folder):
            self.__process_file(file, substringInFilename, newSubstringInFilename, conflictResolveMode)

    @GeneralUtilities.check_arguments
    def __check_file(self, file: str, searchstring: str) -> None:
        bytes_ascii = bytes(searchstring, "ascii")
        bytes_utf16 = bytes(searchstring, "utf-16")  # often called "unicode-encoding"
        bytes_utf8 = bytes(searchstring, "utf-8")
        with open(file, mode='rb') as file_object:
            content = file_object.read()
            if bytes_ascii in content:
                GeneralUtilities.write_message_to_stdout(file)
            elif bytes_utf16 in content:
                GeneralUtilities.write_message_to_stdout(file)
            elif bytes_utf8 in content:
                GeneralUtilities.write_message_to_stdout(file)

    @GeneralUtilities.check_arguments
    def SCSearchInFiles(self, folder: str, searchstring: str) -> None:
        for file in GeneralUtilities.absolute_file_paths(folder):
            self.__check_file(file, searchstring)

    @GeneralUtilities.check_arguments
    def __print_qr_code_by_csv_line(self, displayname: str, website: str, emailaddress: str, key: str, period: str) -> None:
        qrcode_content = f"otpauth://totp/{website}:{emailaddress}?secret={key}&issuer={displayname}&period={period}"
        GeneralUtilities.write_message_to_stdout(f"{displayname} ({emailaddress}):")
        GeneralUtilities.write_message_to_stdout(qrcode_content)
        self.run_program("qr", qrcode_content)

    @GeneralUtilities.check_arguments
    def SCShow2FAAsQRCode(self, csvfile: str) -> None:
        separator_line = "--------------------------------------------------------"
        for line in GeneralUtilities.read_csv_file(csvfile, True):
            GeneralUtilities.write_message_to_stdout(separator_line)
            self.__print_qr_code_by_csv_line(line[0], line[1], line[2], line[3], line[4])
        GeneralUtilities.write_message_to_stdout(separator_line)

    @GeneralUtilities.check_arguments
    def SCUpdateNugetpackagesInCsharpProject(self, csprojfile: str) -> int:
        outdated_packages = self.get_nuget_packages_of_csproj_file(csprojfile, True)
        GeneralUtilities.write_message_to_stdout("The following packages will be updated:")
        for outdated_package in outdated_packages:
            GeneralUtilities.write_message_to_stdout(outdated_package)
            self.update_nuget_package(csprojfile, outdated_package)
        GeneralUtilities.write_message_to_stdout(f"{len(outdated_packages)} package(s) were updated")
        return len(outdated_packages) > 0

    @GeneralUtilities.check_arguments
    def SCUploadFileToFileHost(self, file: str, host: str) -> int:
        try:
            GeneralUtilities.write_message_to_stdout(self.upload_file_to_file_host(file, host))
            return 0
        except Exception as exception:
            GeneralUtilities.write_exception_to_stderr_with_traceback(exception, traceback)
            return 1

    @GeneralUtilities.check_arguments
    def SCFileIsAvailableOnFileHost(self, file: str) -> int:
        try:
            if self.file_is_available_on_file_host(file):
                GeneralUtilities.write_message_to_stdout(f"'{file}' is available")
                return 0
            else:
                GeneralUtilities.write_message_to_stdout(f"'{file}' is not available")
                return 1
        except Exception as exception:
            GeneralUtilities.write_exception_to_stderr_with_traceback(exception, traceback)
            return 2

    @GeneralUtilities.check_arguments
    def SCCalculateBitcoinBlockHash(self, block_version_number: str, previousblockhash: str, transactionsmerkleroot: str, timestamp: str, target: str, nonce: str) -> str:
        # Example-values:
        # block_version_number: "00000020"
        # previousblockhash: "66720b99e07d284bd4fe67ff8c49a5db1dd8514fcdab61000000000000000000"
        # transactionsmerkleroot: "7829844f4c3a41a537b3131ca992643eaa9d093b2383e4cdc060ad7dc5481187"
        # timestamp: "51eb505a"
        # target: "c1910018"
        # nonce: "de19b302"
        header = str(block_version_number + previousblockhash + transactionsmerkleroot + timestamp + target + nonce)
        return binascii.hexlify(hashlib.sha256(hashlib.sha256(binascii.unhexlify(header)).digest()).digest()[::-1]).decode('utf-8')

    @GeneralUtilities.check_arguments
    def SCChangeHashOfProgram(self, inputfile: str) -> None:
        valuetoappend = str(uuid.uuid4())

        outputfile = inputfile + '.modified'

        shutil.copy2(inputfile, outputfile)
        with open(outputfile, 'a', encoding="utf-8") as file:
            # TODO use rcedit for .exe-files instead of appending valuetoappend ( https://github.com/electron/rcedit/ )
            # background: you can retrieve the "original-filename" from the .exe-file like discussed here:
            # https://security.stackexchange.com/questions/210843/ is-it-possible-to-change-original-filename-of-an-exe
            # so removing the original filename with rcedit is probably a better way to make it more difficult to detect the programname.
            # this would obviously also change the hashvalue of the program so appending a whitespace is not required anymore.
            file.write(valuetoappend)

    @GeneralUtilities.check_arguments
    def __adjust_folder_name(self, folder: str) -> str:
        result = os.path.dirname(folder).replace("\\", "/")
        if result == "/":
            return ""
        else:
            return result

    @GeneralUtilities.check_arguments
    def __create_iso(self, folder, iso_file) -> None:
        created_directories = []
        files_directory = "FILES"
        iso = pycdlib.PyCdlib()
        iso.new()
        files_directory = files_directory.upper()
        iso.add_directory("/" + files_directory)
        created_directories.append("/" + files_directory)
        for root, _, files in os.walk(folder):
            for file in files:
                full_path = os.path.join(root, file)
                with (open(full_path, "rb").read()) as text_io_wrapper:
                    content = text_io_wrapper
                    path_in_iso = '/' + files_directory + self.__adjust_folder_name(full_path[len(folder)::1]).upper()
                    if path_in_iso not in created_directories:
                        iso.add_directory(path_in_iso)
                        created_directories.append(path_in_iso)
                    iso.add_fp(BytesIO(content), len(content), path_in_iso + '/' + file.upper() + ';1')
        iso.write(iso_file)
        iso.close()

    @GeneralUtilities.check_arguments
    def SCCreateISOFileWithObfuscatedFiles(self, inputfolder: str, outputfile: str, printtableheadline, createisofile, extensions) -> None:
        if (os.path.isdir(inputfolder)):
            namemappingfile = "name_map.csv"
            files_directory = inputfolder
            files_directory_obf = files_directory + "_Obfuscated"
            self.SCObfuscateFilesFolder(inputfolder, printtableheadline, namemappingfile, extensions)
            os.rename(namemappingfile, os.path.join(files_directory_obf, namemappingfile))
            if createisofile:
                self.__create_iso(files_directory_obf, outputfile)
                shutil.rmtree(files_directory_obf)
        else:
            raise Exception(f"Directory not found: '{inputfolder}'")

    @GeneralUtilities.check_arguments
    def SCFilenameObfuscator(self, inputfolder: str, printtableheadline, namemappingfile: str, extensions: str) -> None:
        obfuscate_all_files = extensions == "*"
        if (not obfuscate_all_files):
            obfuscate_file_extensions = extensions.split(",")

        if (os.path.isdir(inputfolder)):
            printtableheadline = GeneralUtilities.string_to_boolean(printtableheadline)
            files = []
            if not os.path.isfile(namemappingfile):
                with open(namemappingfile, "a", encoding="utf-8"):
                    pass
            if printtableheadline:
                GeneralUtilities.append_line_to_file(namemappingfile, "Original filename;new filename;SHA2-hash of file")
            for file in GeneralUtilities.absolute_file_paths(inputfolder):
                if os.path.isfile(os.path.join(inputfolder, file)):
                    if obfuscate_all_files or self.__extension_matchs(file, obfuscate_file_extensions):
                        files.append(file)
            for file in files:
                hash_value = GeneralUtilities.get_sha256_of_file(file)
                extension = Path(file).suffix
                new_file_name_without_path = str(uuid.uuid4())[0:8] + extension
                new_file_name = os.path.join(os.path.dirname(file), new_file_name_without_path)
                os.rename(file, new_file_name)
                GeneralUtilities.append_line_to_file(namemappingfile, os.path.basename(file) + ";" + new_file_name_without_path + ";" + hash_value)
        else:
            raise Exception(f"Directory not found: '{inputfolder}'")

    @GeneralUtilities.check_arguments
    def __extension_matchs(self, file: str, obfuscate_file_extensions) -> bool:
        for extension in obfuscate_file_extensions:
            if file.lower().endswith("."+extension.lower()):
                return True
        return False

    @GeneralUtilities.check_arguments
    def SCHealthcheck(self, file: str) -> int:
        lines = GeneralUtilities.read_lines_from_file(file)
        for line in reversed(lines):
            if not GeneralUtilities.string_is_none_or_whitespace(line):
                if "RunningHealthy (" in line:  # TODO use regex
                    GeneralUtilities.write_message_to_stderr(f"Healthy running due to line '{line}' in file '{file}'.")
                    return 0
                else:
                    GeneralUtilities.write_message_to_stderr(f"Not healthy running due to line '{line}' in file '{file}'.")
                    return 1
        GeneralUtilities.write_message_to_stderr(f"No valid line found for healthycheck in file '{file}'.")
        return 2

    @GeneralUtilities.check_arguments
    def SCObfuscateFilesFolder(self, inputfolder: str, printtableheadline, namemappingfile: str, extensions: str) -> None:
        obfuscate_all_files = extensions == "*"
        if (not obfuscate_all_files):
            if "," in extensions:
                obfuscate_file_extensions = extensions.split(",")
            else:
                obfuscate_file_extensions = [extensions]
        newd = inputfolder+"_Obfuscated"
        shutil.copytree(inputfolder, newd)
        inputfolder = newd
        if (os.path.isdir(inputfolder)):
            for file in GeneralUtilities.absolute_file_paths(inputfolder):
                if obfuscate_all_files or self.__extension_matchs(file, obfuscate_file_extensions):
                    self.SCChangeHashOfProgram(file)
                    os.remove(file)
                    os.rename(file + ".modified", file)
            self.SCFilenameObfuscator(inputfolder, printtableheadline, namemappingfile, extensions)
        else:
            raise Exception(f"Directory not found: '{inputfolder}'")

    @GeneralUtilities.check_arguments
    def upload_file_to_file_host(self, file: str, host: str) -> int:
        if (host is None):
            return self.upload_file_to_random_filesharing_service(file)
        elif host == "anonfiles.com":
            return self.upload_file_to_anonfiles(file)
        elif host == "bayfiles.com":
            return self.upload_file_to_bayfiles(file)
        GeneralUtilities.write_message_to_stderr("Unknown host: "+host)
        return 1

    @GeneralUtilities.check_arguments
    def upload_file_to_random_filesharing_service(self, file: str) -> int:
        host = randrange(2)
        if host == 0:
            return self.upload_file_to_anonfiles(file)
        if host == 1:
            return self.upload_file_to_bayfiles(file)
        return 1

    @GeneralUtilities.check_arguments
    def upload_file_to_anonfiles(self, file) -> int:
        return self.upload_file_by_using_simple_curl_request("https://api.anonfiles.com/upload", file)

    @GeneralUtilities.check_arguments
    def upload_file_to_bayfiles(self, file) -> int:
        return self.upload_file_by_using_simple_curl_request("https://api.bayfiles.com/upload", file)

    @GeneralUtilities.check_arguments
    def upload_file_by_using_simple_curl_request(self, api_url: str, file: str) -> int:
        # TODO implement
        return 1

    @GeneralUtilities.check_arguments
    def file_is_available_on_file_host(self, file) -> int:
        # TODO implement
        return 1

    def run_testcases_for_python_project(self, repository_folder: str):
        self.run_program("coverage", "run -m pytest", repository_folder)
        self.run_program("coverage", "xml", repository_folder)
        GeneralUtilities.ensure_directory_exists(os.path.join(repository_folder, "Other/TestCoverage"))
        coveragefile = os.path.join(repository_folder, "Other/TestCoverage/TestCoverage.xml")
        GeneralUtilities.ensure_file_does_not_exist(coveragefile)
        os.rename(os.path.join(repository_folder, "coverage.xml"), coveragefile)

    @GeneralUtilities.check_arguments
    def get_nuget_packages_of_csproj_file(self, csproj_file: str, only_outdated_packages: bool) -> bool:
        self.run_program("dotnet", f'restore --disable-parallel --force --force-evaluate "{csproj_file}"')
        if only_outdated_packages:
            only_outdated_packages_argument = " --outdated"
        else:
            only_outdated_packages_argument = ""
        stdout = self.run_program("dotnet", f'list "{csproj_file}" package{only_outdated_packages_argument}')[1]
        result = []
        for line in stdout.splitlines():
            trimmed_line = line.replace("\t", "").strip()
            if trimmed_line.startswith(">"):
                result.append(trimmed_line[2:].split(" ")[0])
        return result

    @GeneralUtilities.check_arguments
    def update_nuget_package(self, csproj_file: str, name: str) -> None:
        self.run_program("dotnet", f'add "{csproj_file}" package {name}')

    @GeneralUtilities.check_arguments
    def get_file_permission(self, file: str) -> str:
        """This function returns an usual octet-triple, for example "0700"."""
        ls_output = self.__ls(file)
        return self.__get_file_permission_helper(ls_output)

    @GeneralUtilities.check_arguments
    def __get_file_permission_helper(self, ls_output: str) -> str:
        permissions = ' '.join(ls_output.split()).split(' ')[0][1:]
        return str(self.__to_octet(permissions[0:3]))+str(self.__to_octet(permissions[3:6]))+str(self.__to_octet(permissions[6:9]))

    @GeneralUtilities.check_arguments
    def __to_octet(self, string: str) -> int:
        return int(self.__to_octet_helper(string[0])+self.__to_octet_helper(string[1])+self.__to_octet_helper(string[2]), 2)

    @GeneralUtilities.check_arguments
    def __to_octet_helper(self, string: str) -> str:
        if (string == "-"):
            return "0"
        else:
            return "1"

    @GeneralUtilities.check_arguments
    def get_file_owner(self, file: str) -> str:
        """This function returns the user and the group in the format "user:group"."""
        ls_output = self.__ls(file)
        return self.__get_file_owner_helper(ls_output)

    @GeneralUtilities.check_arguments
    def __get_file_owner_helper(self, ls_output: str) -> str:
        try:
            splitted = ' '.join(ls_output.split()).split(' ')
            return f"{splitted[2]}:{splitted[3]}"
        except Exception as exception:
            raise ValueError(f"ls-output '{ls_output}' not parsable") from exception

    @GeneralUtilities.check_arguments
    def get_file_owner_and_file_permission(self, file: str) -> str:
        ls_output = self.__ls(file)
        return [self.__get_file_owner_helper(ls_output), self.__get_file_permission_helper(ls_output)]

    @GeneralUtilities.check_arguments
    def __ls(self, file: str) -> str:
        file = file.replace("\\", "/")
        GeneralUtilities.assert_condition(os.path.isfile(file) or os.path.isdir(file), f"Can not execute 'ls' because '{file}' does not exist")
        result = self.run_program_argsasarray("ls", ["-ld", file])
        GeneralUtilities.assert_condition(result[0] == 0, f"'ls -ld {file}' resulted in exitcode {str(result[0])}. StdErr: {result[2]}")
        GeneralUtilities.assert_condition(not GeneralUtilities.string_is_none_or_whitespace(result[1]), f"'ls' of '{file}' had an empty output. StdErr: '{result[2]}'")
        return result[1]

    @GeneralUtilities.check_arguments
    def set_permission(self, file_or_folder: str, permissions: str, recursive: bool = False) -> None:
        """This function expects an usual octet-triple, for example "700"."""
        args = []
        if recursive:
            args.append("--recursive")
        args.append(permissions)
        args.append(file_or_folder)
        self.run_program_argsasarray("chmod", args)

    @GeneralUtilities.check_arguments
    def set_owner(self, file_or_folder: str, owner: str, recursive: bool = False, follow_symlinks: bool = False) -> None:
        """This function expects the user and the group in the format "user:group"."""
        args = []
        if recursive:
            args.append("--recursive")
        if follow_symlinks:
            args.append("--no-dereference")
        args.append(owner)
        args.append(file_or_folder)
        self.run_program_argsasarray("chown", args)

    # <run programs>

    @GeneralUtilities.check_arguments
    def __run_program_argsasarray_async_helper(self, program: str, arguments_as_array: list[str] = [], working_directory: str = None, verbosity: int = 1,
                                               print_errors_as_information: bool = False, log_file: str = None, timeoutInSeconds: int = 600, addLogOverhead: bool = False,
                                               title: str = None, log_namespace: str = "", arguments_for_log:  list[str] = None, custom_argument: object = None) -> Popen:
        # Verbosity:
        # 0=Quiet (No output will be printed.)
        # 1=Normal (If the exitcode of the executed program is not 0 then the StdErr will be printed.)
        # 2=Full (Prints StdOut and StdErr of the executed program.)
        # 3=Verbose (Same as "Full" but with some more information.)

        if arguments_for_log is None:
            arguments_for_log = ' '.join(arguments_as_array)
        else:
            arguments_for_log = ' '.join(arguments_for_log)
        working_directory = self.__adapt_workingdirectory(working_directory)
        cmd = f'{working_directory}>{program} {arguments_for_log}'

        if GeneralUtilities.string_is_none_or_whitespace(title):
            info_for_log = cmd
        else:
            info_for_log = title

        if verbosity >= 3:
            GeneralUtilities.write_message_to_stdout(f"Run '{info_for_log}'.")

        if isinstance(self.program_runner, ProgramRunnerEpew):
            custom_argument = CustomEpewArgument(print_errors_as_information, log_file, timeoutInSeconds, addLogOverhead, title, log_namespace, verbosity, arguments_for_log)
        popen: Popen = self.program_runner.run_program_argsasarray_async_helper(program, arguments_as_array, working_directory, custom_argument)
        return popen

    # Return-values program_runner: Exitcode, StdOut, StdErr, Pid

    @GeneralUtilities.check_arguments
    def run_program_argsasarray(self, program: str, arguments_as_array: list[str] = [], working_directory: str = None, verbosity: int = 1,
                                print_errors_as_information: bool = False, log_file: str = None, timeoutInSeconds: int = 600, addLogOverhead: bool = False,
                                title: str = None, log_namespace: str = "", arguments_for_log:  list[str] = None,
                                throw_exception_if_exitcode_is_not_zero: bool = True, custom_argument: object = None) -> tuple[int, str, str, int]:
        mock_loader_result = self.__try_load_mock(program, ' '.join(arguments_as_array), working_directory)
        if mock_loader_result[0]:
            return mock_loader_result[1]

        start_datetime = datetime.utcnow()

        if arguments_for_log is None:
            arguments_for_log = arguments_as_array

        arguments_for_log_as_string = ' '.join(arguments_for_log)
        cmd = f'{working_directory}>{program} {arguments_for_log_as_string}'
        if GeneralUtilities.string_is_none_or_whitespace(title):
            info_for_log = cmd
        else:
            info_for_log = title

        epew_will_be_used = isinstance(self.program_runner, ProgramRunnerEpew)
        program_manages_logging_itself = epew_will_be_used
        program_manages_output_itself = epew_will_be_used

        process = self.__run_program_argsasarray_async_helper(program, arguments_as_array, working_directory, verbosity, print_errors_as_information, log_file,
                                                              timeoutInSeconds, addLogOverhead, title, log_namespace, arguments_for_log, custom_argument)
        pid = process.pid

        if program_manages_output_itself:
            for c in iter(lambda: process.stdout.read(1), b""):
                sys.stdout.buffer.write(c)
            for c in iter(lambda: process.stderr.read(1), b""):
                sys.stderr.buffer.write(c)

        stdout, stderr = process.communicate()
        exit_code = process.wait()
        stdout = GeneralUtilities.bytes_to_string(stdout).replace('\r', '')
        stderr = GeneralUtilities.bytes_to_string(stderr).replace('\r', '')
        end_datetime = datetime.utcnow()

        if arguments_for_log is None:
            arguments_for_log = ' '.join(arguments_as_array)
        else:
            arguments_for_log = ' '.join(arguments_for_log)

        duration: timedelta = end_datetime-start_datetime

        if GeneralUtilities.string_is_none_or_whitespace(title):
            info_for_log = cmd
        else:
            info_for_log = title

        if not program_manages_logging_itself and log_file is not None:
            GeneralUtilities.ensure_file_exists(log_file)
            GeneralUtilities.append_line_to_file(log_file, stdout)
            GeneralUtilities.append_line_to_file(log_file, stderr)

        if not program_manages_output_itself:
            if verbosity == 1 and exit_code != 0:
                self.__write_error_output(print_errors_as_information, stderr)
            if verbosity == 2:
                GeneralUtilities.write_message_to_stdout(stdout)
                self.__write_error_output(print_errors_as_information, stderr)
            if verbosity == 3:
                GeneralUtilities.write_message_to_stdout(stdout)
                self.__write_error_output(print_errors_as_information, stderr)
                formatted = self.__format_program_execution_information(title=info_for_log, program=program, argument=arguments_for_log, workingdirectory=working_directory)
                GeneralUtilities.write_message_to_stdout(f"Finished '{info_for_log}'. Details: '{formatted}")

        if throw_exception_if_exitcode_is_not_zero and exit_code != 0:
            formatted = self.__format_program_execution_information(exit_code, stdout, stderr, program, arguments_for_log, working_directory, info_for_log, pid, duration)
            raise ValueError(f"Finished '{info_for_log}'. Details: '{formatted}")

        result = (exit_code, stdout, stderr, pid)
        return result

    # Return-values program_runner: Exitcode, StdOut, StdErr, Pid
    @GeneralUtilities.check_arguments
    def run_program(self, program: str, arguments:  str = "", working_directory: str = None, verbosity: int = 1,
                    print_errors_as_information: bool = False, log_file: str = None, timeoutInSeconds: int = 600, addLogOverhead: bool = False,
                    title: str = None, log_namespace: str = "", arguments_for_log:  list[str] = None, throw_exception_if_exitcode_is_not_zero: bool = True,
                    custom_argument: object = None) -> tuple[int, str, str, int]:
        return self.run_program_argsasarray(program, GeneralUtilities.arguments_to_array(arguments), working_directory, verbosity, print_errors_as_information,
                                            log_file, timeoutInSeconds, addLogOverhead, title, log_namespace, arguments_for_log, throw_exception_if_exitcode_is_not_zero, custom_argument)

    # Return-values program_runner: Pid
    @GeneralUtilities.check_arguments
    def run_program_argsasarray_async(self, program: str, arguments_as_array: list[str] = [], working_directory: str = None, verbosity: int = 1,
                                      print_errors_as_information: bool = False, log_file: str = None, timeoutInSeconds: int = 600, addLogOverhead: bool = False,
                                      title: str = None, log_namespace: str = "", arguments_for_log:  list[str] = None, custom_argument: object = None) -> int:
        mock_loader_result = self.__try_load_mock(program, ' '.join(arguments_as_array), working_directory)
        if mock_loader_result[0]:
            return mock_loader_result[1]

        process: Popen = self.__run_program_argsasarray_async_helper(program, arguments_as_array, working_directory, verbosity,
                                                                     print_errors_as_information, log_file, timeoutInSeconds, addLogOverhead, title, log_namespace, arguments_for_log, custom_argument)
        return process.pid

    # Return-values program_runner: Pid
    @GeneralUtilities.check_arguments
    def run_program_async(self, program: str, arguments: str = "",  working_directory: str = None, verbosity: int = 1,
                          print_errors_as_information: bool = False, log_file: str = None, timeoutInSeconds: int = 600, addLogOverhead: bool = False,
                          title: str = None, log_namespace: str = "", arguments_for_log:  list[str] = None, custom_argument: object = None) -> int:
        return self.run_program_argsasarray_async(program, GeneralUtilities.arguments_to_array(arguments), working_directory, verbosity,
                                                  print_errors_as_information, log_file, timeoutInSeconds, addLogOverhead, title, log_namespace, arguments_for_log, custom_argument)

    @GeneralUtilities.check_arguments
    def __try_load_mock(self, program: str, arguments: str, working_directory: str) -> tuple[bool, tuple[int, str, str, int]]:
        if self.mock_program_calls:
            try:
                return [True, self.__get_mock_program_call(program, arguments, working_directory)]
            except LookupError:
                if not self.execute_program_really_if_no_mock_call_is_defined:
                    raise
        return [False, None]

    @GeneralUtilities.check_arguments
    def __adapt_workingdirectory(self, workingdirectory: str) -> str:
        if workingdirectory is None:
            return os.getcwd()
        else:
            return GeneralUtilities.resolve_relative_path_from_current_working_directory(workingdirectory)

    @GeneralUtilities.check_arguments
    def __write_error_output(self, print_errors_as_information, stderr):
        if print_errors_as_information:
            GeneralUtilities.write_message_to_stdout(stderr)
        else:
            GeneralUtilities.write_message_to_stderr(stderr)

    @GeneralUtilities.check_arguments
    def __format_program_execution_information(self, exitcode: int = None,  stdout: str = None, stderr: str = None, program: str = None, argument: str = None,
                                               workingdirectory: str = None, title: str = None, pid: int = None, execution_duration: timedelta = None):
        result = ""
        if (exitcode is not None and stdout is not None and stderr is not None):
            result = f"{result} Exitcode: {exitcode}; StdOut: '{stdout}'; StdErr: '{stderr}'"
        if (pid is not None):
            result = f"Pid: '{pid}'; {result}"
        if (program is not None and argument is not None and workingdirectory is not None):
            result = f"Command: '{workingdirectory}> {program} {argument}'; {result}"
        if (execution_duration is not None):
            result = f"{result}; Duration: '{str(execution_duration)}'"
        if (title is not None):
            result = f"Title: '{title}'; {result}"
        return result.strip()

    @GeneralUtilities.check_arguments
    def verify_no_pending_mock_program_calls(self):
        if (len(self.__mocked_program_calls) > 0):
            raise AssertionError(
                "The following mock-calls were not called:\n"+",\n    ".join([self.__format_mock_program_call(r) for r in self.__mocked_program_calls]))

    @GeneralUtilities.check_arguments
    def __format_mock_program_call(self, r) -> str:
        r: ScriptCollectionCore.__MockProgramCall = r
        return f"'{r.workingdirectory}>{r.program} {r.argument}' (" \
            f"exitcode: {GeneralUtilities.str_none_safe(str(r.exit_code))}, " \
            f"pid: {GeneralUtilities.str_none_safe(str(r.pid))}, "\
            f"stdout: {GeneralUtilities.str_none_safe(str(r.stdout))}, " \
            f"stderr: {GeneralUtilities.str_none_safe(str(r.stderr))})"

    @GeneralUtilities.check_arguments
    def register_mock_program_call(self, program: str, argument: str, workingdirectory: str, result_exit_code: int, result_stdout: str, result_stderr: str,
                                   result_pid: int, amount_of_expected_calls=1):
        "This function is for test-purposes only"
        for _ in itertools.repeat(None, amount_of_expected_calls):
            mock_call = ScriptCollectionCore.__MockProgramCall()
            mock_call.program = program
            mock_call.argument = argument
            mock_call.workingdirectory = workingdirectory
            mock_call.exit_code = result_exit_code
            mock_call.stdout = result_stdout
            mock_call.stderr = result_stderr
            mock_call.pid = result_pid
            self.__mocked_program_calls.append(mock_call)

    @GeneralUtilities.check_arguments
    def __get_mock_program_call(self, program: str, argument: str, workingdirectory: str):
        result: ScriptCollectionCore.__MockProgramCall = None
        for mock_call in self.__mocked_program_calls:
            if ((re.match(mock_call.program, program) is not None)
               and (re.match(mock_call.argument, argument) is not None)
               and (re.match(mock_call.workingdirectory, workingdirectory) is not None)):
                result = mock_call
                break
        if result is None:
            raise LookupError(f"Tried to execute mock-call '{workingdirectory}>{program} {argument}' but no mock-call was defined for that execution")
        else:
            self.__mocked_program_calls.remove(result)
            return (result.exit_code, result.stdout, result.stderr, result.pid)

    @GeneralUtilities.check_arguments
    class __MockProgramCall:
        program: str
        argument: str
        workingdirectory: str
        exit_code: int
        stdout: str
        stderr: str
        pid: int

    # </run programs>

    @GeneralUtilities.check_arguments
    def extract_archive_with_7z(self, unzip_program_file: str, zipfile: str, password: str, output_directory: str) -> None:
        password_set = not password is None
        file_name = Path(zipfile).name
        file_folder = os.path.dirname(zipfile)
        argument = "x"
        if password_set:
            argument = f"{argument} -p\"{password}\""
        argument = f"{argument} -o {output_directory}"
        argument = f"{argument} {file_name}"
        return self.run_program(unzip_program_file, argument, file_folder)

    @GeneralUtilities.check_arguments
    def get_internet_time(self) -> datetime:
        response = ntplib.NTPClient().request('pool.ntp.org')
        return datetime.fromtimestamp(response.tx_time)

    @GeneralUtilities.check_arguments
    def system_time_equals_internet_time(self, maximal_tolerance_difference: timedelta) -> bool:
        return abs(datetime.now() - self.get_internet_time()) < maximal_tolerance_difference

    @GeneralUtilities.check_arguments
    def system_time_equals_internet_time_with_default_tolerance(self) -> bool:
        return self.system_time_equals_internet_time(self.__get_default_tolerance_for_system_time_equals_internet_time())

    @GeneralUtilities.check_arguments
    def check_system_time(self, maximal_tolerance_difference: timedelta):
        if not self.system_time_equals_internet_time(maximal_tolerance_difference):
            raise ValueError("System time may be wrong")

    @GeneralUtilities.check_arguments
    def check_system_time_with_default_tolerance(self) -> None:
        self.check_system_time(self.__get_default_tolerance_for_system_time_equals_internet_time())

    @GeneralUtilities.check_arguments
    def __get_default_tolerance_for_system_time_equals_internet_time(self) -> timedelta:
        return timedelta(hours=0, minutes=0, seconds=3)

    @GeneralUtilities.check_arguments
    def get_semver_version_from_gitversion(self, folder: str) -> str:
        return self.get_version_from_gitversion(folder, "MajorMinorPatch")

    @GeneralUtilities.check_arguments
    def get_version_from_gitversion(self, folder: str, variable: str) -> str:
        # called twice as workaround for issue 1877 in gitversion ( https://github.com/GitTools/GitVersion/issues/1877 )
        result = self.run_program_argsasarray("gitversion", ["/showVariable", variable], folder)
        result = self.run_program_argsasarray("gitversion", ["/showVariable", variable], folder)
        return GeneralUtilities.strip_new_line_character(result[1])

    @GeneralUtilities.check_arguments
    def generate_certificate_authority(self, folder: str, name: str, subj_c: str, subj_st: str, subj_l: str, subj_o: str, subj_ou: str,
                                       days_until_expire: int = None, password: str = None) -> None:
        if days_until_expire is None:
            days_until_expire = 1825
        if password is None:
            password = GeneralUtilities.generate_password()
        self.run_program("openssl", f'req -new -newkey ec -pkeyopt ec_paramgen_curve:prime256v1 -days {days_until_expire} -nodes -x509 -subj ' +
                         f'/C={subj_c}/ST={subj_st}/L={subj_l}/O={subj_o}/CN={name}/OU={subj_ou} -passout pass:{password} ' +
                         f'-keyout {name}.key -out {name}.crt', folder)

    @GeneralUtilities.check_arguments
    def generate_certificate(self, folder: str, domain: str, subj_c: str, subj_st: str, subj_l: str, subj_o: str, subj_ou: str,
                             days_until_expire: int = None, password: str = None) -> None:
        if days_until_expire is None:
            days_until_expire = 397
        if password is None:
            password = GeneralUtilities.generate_password()
        rsa_key_length = 4096
        self.run_program("openssl", f'genrsa -out {domain}.key {rsa_key_length}', folder)
        self.run_program("openssl", f'req -new -subj /C={subj_c}/ST={subj_st}/L={subj_l}/O={subj_o}/CN={domain}/OU={subj_ou} -x509 ' +
                         f'-key {domain}.key -out {domain}.unsigned.crt -days {days_until_expire}', folder)
        self.run_program("openssl", f'pkcs12 -export -out {domain}.pfx -password pass:{password} -inkey {domain}.key -in {domain}.unsigned.crt', folder)
        GeneralUtilities.write_text_to_file(os.path.join(folder, f"{domain}.password"), password)
        GeneralUtilities.write_text_to_file(os.path.join(folder, f"{domain}.san.conf"), f"""[ req ]
default_bits        = {rsa_key_length}
distinguished_name  = req_distinguished_name
req_extensions      = v3_req
default_md          = sha256
dirstring_type      = nombstr
prompt              = no

[ req_distinguished_name ]
countryName         = {subj_c}
stateOrProvinceName = {subj_st}
localityName        = {subj_l}
organizationName    = {subj_o}
organizationUnit    = {subj_ou}
commonName          = {domain}

[v3_req]
subjectAltName      = @subject_alt_name

[ subject_alt_name ]
DNS                 = {domain}
""")

    @GeneralUtilities.check_arguments
    def generate_certificate_sign_request(self, folder: str, domain: str, subj_c: str, subj_st: str, subj_l: str, subj_o: str, subj_ou: str) -> None:
        self.run_program("openssl", f'req -new -subj /C={subj_c}/ST={subj_st}/L={subj_l}/O={subj_o}/CN={domain}/OU={subj_ou} ' +
                         f'-key {domain}.key -out {domain}.csr -config {domain}.san.conf', folder)

    @GeneralUtilities.check_arguments
    def sign_certificate(self, folder: str, ca_folder: str, ca_name: str, domain: str, days_until_expire: int = None) -> None:
        if days_until_expire is None:
            days_until_expire = 397
        ca = os.path.join(ca_folder, ca_name)
        self.run_program("openssl", f'x509 -req -in {domain}.csr -CA {ca}.crt -CAkey {ca}.key -CAserial {ca}.srl ' +
                         f'-out {domain}.crt -days {days_until_expire} -sha256 -extensions v3_req -extfile {domain}.san.conf', folder)
