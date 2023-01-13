from datetime import datetime
from graphlib import TopologicalSorter
import os
from pathlib import Path
import shutil
import re
import tempfile
import json
import configparser
import xmlschema
from lxml import etree
from .GeneralUtilities import GeneralUtilities
from .ScriptCollectionCore import ScriptCollectionCore
from .ProgramRunnerEpew import ProgramRunnerEpew


class CreateReleaseConfiguration():
    projectname: str
    remotename: str
    artifacts_folder: str
    push_artifacts_scripts_folder: str
    verbosity: int
    reference_repository_remote_name: str = None
    reference_repository_branch_name: str = "main"
    build_repository_branch: str = "main"
    public_repository_url: str
    additional_arguments_file: str = None

    def __init__(self, projectname: str, remotename: str, build_artifacts_target_folder: str, push_artifacts_scripts_folder: str,
                 verbosity: int, public_repository_url: str, additional_arguments_file: str):

        self.projectname = projectname
        self.remotename = remotename
        self.artifacts_folder = build_artifacts_target_folder
        self.push_artifacts_scripts_folder = push_artifacts_scripts_folder
        self.verbosity = verbosity
        self.public_repository_url = public_repository_url
        self.reference_repository_remote_name = self.remotename
        self.additional_arguments_file = additional_arguments_file


class CreateReleaseInformationForProjectInCommonProjectFormat:
    projectname: str
    repository: str
    artifacts_folder: str
    verbosity: int = 1
    reference_repository: str = None
    public_repository_url: str = None
    target_branch_name: str = None
    push_artifacts_scripts_folder: str = None
    target_environmenttype_for_qualitycheck: str = "QualityCheck"
    target_environmenttype_for_productive: str = "Productive"
    additional_arguments_file: str = None
    export_target: str = None

    def __init__(self, repository: str, artifacts_folder: str, projectname: str, public_repository_url: str,
                 target_branch_name: str, additional_arguments_file: str, export_target: str, push_artifacts_scripts_folder: str):
        self.repository = repository
        self.public_repository_url = public_repository_url
        self.target_branch_name = target_branch_name
        self.artifacts_folder = artifacts_folder
        self.additional_arguments_file = additional_arguments_file
        self.export_target = export_target
        self.push_artifacts_scripts_folder = push_artifacts_scripts_folder
        if projectname is None:
            projectname = os.path.basename(self.repository)
        else:
            self.projectname = projectname
        self.reference_repository = GeneralUtilities.resolve_relative_path(f"../{projectname}Reference", repository)


class MergeToStableBranchInformationForProjectInCommonProjectFormat:
    repository: str
    sourcebranch: str = "main"
    targetbranch: str = "stable"
    sign_git_tags: bool = True
    target_environmenttype_for_qualitycheck: str = "QualityCheck"
    target_environmenttype_for_productive: str = "Productive"
    additional_arguments_file: str = None
    export_target: str = None

    push_source_branch: bool = False
    push_source_branch_remote_name: str = None
    push_target_branch: bool = False
    push_target_branch_remote_name: str = None

    verbosity: int = 1

    def __init__(self, repository: str, additional_arguments_file: str, export_target: str):
        self.repository = repository
        self.additional_arguments_file = additional_arguments_file
        self.export_target = export_target


class TasksForCommonProjectStructure:
    __sc: ScriptCollectionCore = None
    reference_latest_version_of_xsd_when_generating_xml: bool = True

    @staticmethod
    @GeneralUtilities.check_arguments
    def get_development_environment_name() -> str:
        return "Development"

    @staticmethod
    @GeneralUtilities.check_arguments
    def get_qualitycheck_environment_name() -> str:
        return "QualityCheck"

    @staticmethod
    @GeneralUtilities.check_arguments
    def get_productive_environment_name() -> str:
        return "Productive"

    def __init__(self, sc: ScriptCollectionCore = None):
        if sc is None:
            sc = ScriptCollectionCore()
        self.__sc = sc

    @GeneralUtilities.check_arguments
    def get_build_folder(self, repository_folder: str, codeunit_name: str) -> str:
        return os.path.join(repository_folder, codeunit_name, "Other", "Build")

    @GeneralUtilities.check_arguments
    def get_artifacts_folder(self, repository_folder: str, codeunit_name: str) -> str:
        return os.path.join(repository_folder, codeunit_name, "Other", "Artifacts")

    @GeneralUtilities.check_arguments
    def get_wheel_file(self, repository_folder: str, codeunit_name: str) -> str:
        return self.__sc.find_file_by_extension(os.path.join(self.get_artifacts_folder(repository_folder, codeunit_name),
                                                             "BuildResult_Wheel"), "whl")

    @GeneralUtilities.check_arguments
    def __get_testcoverage_threshold_from_codeunit_file(self, codeunit_file):
        root: etree._ElementTree = etree.parse(codeunit_file)
        return float(str(root.xpath('//cps:minimalcodecoverageinpercent/text()', namespaces={
            'cps': 'https://projects.aniondev.de/PublicProjects/Common/ProjectTemplates/-/tree/main/Conventions/RepositoryStructure/CommonProjectStructure'
        })[0]))

    @GeneralUtilities.check_arguments
    def check_testcoverage(self, testcoverage_file_in_cobertura_format: str, repository_folder: str, codeunitname: str):
        root: etree._ElementTree = etree.parse(testcoverage_file_in_cobertura_format)
        coverage_in_percent = round(float(str(root.xpath('//coverage/@line-rate')[0]))*100, 2)
        codeunit_file = os.path.join(repository_folder, codeunitname, f"{codeunitname}.codeunit.xml")
        threshold_in_percent = self.__get_testcoverage_threshold_from_codeunit_file(codeunit_file)
        minimalrequiredtestcoverageinpercent = threshold_in_percent
        if (coverage_in_percent < minimalrequiredtestcoverageinpercent):
            raise ValueError(f"The testcoverage must be {minimalrequiredtestcoverageinpercent}% or more but is {coverage_in_percent}%.")

    @GeneralUtilities.check_arguments
    def replace_version_in_python_file(self, file: str, new_version_value: str):
        GeneralUtilities.write_text_to_file(file, re.sub("version = \"\\d+\\.\\d+\\.\\d+\"", f"version = \"{new_version_value}\"",
                                                         GeneralUtilities.read_text_from_file(file)))

    @staticmethod
    @GeneralUtilities.check_arguments
    def __adjust_source_in_testcoverage_file(testcoverage_file: str, codeunitname: str) -> None:
        GeneralUtilities.write_text_to_file(testcoverage_file, re.sub("<source>.+<\\/source>", f"<source>{codeunitname}</source>",
                                                                      GeneralUtilities.read_text_from_file(testcoverage_file)))

    @staticmethod
    @GeneralUtilities.check_arguments
    def update_path_of_source(repository_folder: str, codeunitname: str) -> None:
        folder = f"{repository_folder}/{codeunitname}/Other/Artifacts/TestCoverage"
        filename = "TestCoverage.xml"
        full_file = os.path.join(folder, filename)
        TasksForCommonProjectStructure.__adjust_source_in_testcoverage_file(full_file, codeunitname)

    @GeneralUtilities.check_arguments
    def standardized_tasks_run_testcases_for_python_codeunit(self, run_testcases_file: str, generate_badges: bool, verbosity: int,
                                                             targetenvironmenttype: str, commandline_arguments: list[str]):
        codeunitname: str = Path(os.path.dirname(run_testcases_file)).parent.parent.name
        verbosity = TasksForCommonProjectStructure.get_verbosity_from_commandline_arguments(commandline_arguments,  verbosity)
        repository_folder: str = str(Path(os.path.dirname(run_testcases_file)).parent.parent.parent.absolute())
        codeunit_folder = os.path.join(repository_folder, codeunitname)
        self.__sc.run_program("coverage", "run -m pytest", codeunit_folder,  verbosity=verbosity)
        self.__sc.run_program("coverage", "xml", codeunit_folder, verbosity=verbosity)
        coveragefolder = os.path.join(repository_folder, codeunitname, "Other/Artifacts/TestCoverage")
        GeneralUtilities.ensure_directory_exists(coveragefolder)
        coveragefile = os.path.join(coveragefolder, "TestCoverage.xml")
        GeneralUtilities.ensure_file_does_not_exist(coveragefile)
        os.rename(os.path.join(repository_folder, codeunitname, "coverage.xml"), coveragefile)
        self.update_path_of_source(repository_folder, codeunitname)
        self.standardized_tasks_generate_coverage_report(repository_folder, codeunitname, verbosity, generate_badges, targetenvironmenttype, commandline_arguments)
        self.check_testcoverage(coveragefile, repository_folder, codeunitname)

    @GeneralUtilities.check_arguments
    def standardized_tasks_build_for_python_codeunit(self, buildscript_file: str, verbosity: int, targetenvironmenttype: str, commandline_arguments: list[str]):
        codeunitname: str = Path(os.path.dirname(buildscript_file)).parent.parent.name
        verbosity = TasksForCommonProjectStructure.get_verbosity_from_commandline_arguments(commandline_arguments,  verbosity)
        codeunit_folder = str(Path(os.path.dirname(buildscript_file)).parent.parent.absolute())
        repository_folder: str = str(Path(os.path.dirname(buildscript_file)).parent.parent.parent.absolute())
        target_directory = GeneralUtilities.resolve_relative_path(
            "../Artifacts/BuildResult_Wheel", os.path.join(self.get_artifacts_folder(repository_folder, codeunitname)))
        GeneralUtilities.ensure_directory_exists(target_directory)
        self.__sc.run_program("python", f"-m build --wheel --outdir {target_directory}", codeunit_folder, verbosity=verbosity)

    @GeneralUtilities.check_arguments
    def standardized_tasks_push_wheel_file_to_registry(self, wheel_file: str, api_key: str, repository: str, gpg_identity: str, verbosity: int) -> None:
        # repository-value when PyPi should be used: "pypi"
        # gpg_identity-value when wheel-file should not be signed: None
        folder = os.path.dirname(wheel_file)
        filename = os.path.basename(wheel_file)

        if gpg_identity is None:
            gpg_identity_argument = ""
        else:
            gpg_identity_argument = f" --sign --identity {gpg_identity}"

        if verbosity > 2:
            verbose_argument = " --verbose"
        else:
            verbose_argument = ""

        twine_argument = f"upload{gpg_identity_argument} --repository {repository} --non-interactive {filename} --disable-progress-bar"
        twine_argument = f"{twine_argument} --username __token__ --password {api_key}{verbose_argument}"
        self.__sc.run_program("twine", twine_argument, folder, verbosity=verbosity, throw_exception_if_exitcode_is_not_zero=True)

    @GeneralUtilities.check_arguments
    def push_wheel_build_artifact(self, push_build_artifacts_file, product_name, codeunitname, repository: str,
                                  apikey: str, gpg_identity: str, verbosity: int, commandline_arguments: list[str]) -> None:
        verbosity = TasksForCommonProjectStructure.get_verbosity_from_commandline_arguments(commandline_arguments,  verbosity)
        folder_of_this_file = os.path.dirname(push_build_artifacts_file)
        repository_folder = GeneralUtilities.resolve_relative_path(f"..{os.path.sep}../Submodules{os.path.sep}{product_name}", folder_of_this_file)
        wheel_file = self.get_wheel_file(repository_folder, codeunitname)
        self.standardized_tasks_push_wheel_file_to_registry(wheel_file, apikey, repository, gpg_identity, verbosity)

    @GeneralUtilities.check_arguments
    def get_version_of_codeunit(self, codeunit_file: str) -> None:
        root: etree._ElementTree = etree.parse(codeunit_file)
        result = str(root.xpath('//cps:version/text()',
                     namespaces={'cps': 'https://projects.aniondev.de/PublicProjects/Common/ProjectTemplates/-/tree/main/Conventions/RepositoryStructure/CommonProjectStructure'})[0])
        return result

    @GeneralUtilities.check_arguments
    def get_version_of_codeunit_folder(self, codeunit_folder: str) -> None:
        codeunit_file = os.path.join(codeunit_folder, f"{os.path.basename(codeunit_folder)}.codeunit.xml")
        return self.get_version_of_codeunit(codeunit_file)

    @staticmethod
    @GeneralUtilities.check_arguments
    def get_buildconfigurationdevelopment_from_commandline_arguments(commandline_arguments: list[str], default_value: str) -> str:
        return TasksForCommonProjectStructure.get_string_value_from_commandline_arguments(commandline_arguments, "buildconfigurationdevelopment",  default_value)

    @staticmethod
    @GeneralUtilities.check_arguments
    def get_buildconfigurationqualitycheck_from_commandline_arguments(commandline_arguments: list[str], default_value: str) -> str:
        return TasksForCommonProjectStructure.get_string_value_from_commandline_arguments(commandline_arguments, "buildconfigurationqualitycheck",  default_value)

    @staticmethod
    @GeneralUtilities.check_arguments
    def get_buildconfigurationproductive_from_commandline_arguments(commandline_arguments: list[str],  default_value: str) -> str:
        return TasksForCommonProjectStructure.get_string_value_from_commandline_arguments(commandline_arguments, "buildconfigurationproductive",  default_value)

    @staticmethod
    @GeneralUtilities.check_arguments
    def get_string_value_from_commandline_arguments(commandline_arguments: list[str], property_name: str, default_value: str) -> str:
        result = TasksForCommonProjectStructure.get_property_from_commandline_arguments(commandline_arguments, property_name)
        if result is None:
            return default_value
        else:
            return result

    @staticmethod
    @GeneralUtilities.check_arguments
    def get_is_pre_merge_value_from_commandline_arguments(commandline_arguments: list[str],  default_value: bool) -> bool:
        result = TasksForCommonProjectStructure.get_property_from_commandline_arguments(commandline_arguments, "is_pre_merge")
        if result is None:
            return default_value
        else:
            return GeneralUtilities.string_to_boolean(result)

    @staticmethod
    @GeneralUtilities.check_arguments
    def get_assume_dependent_codeunits_are_already_built_from_commandline_arguments(commandline_arguments: list[str],  default_value: bool) -> bool:
        result = TasksForCommonProjectStructure.get_property_from_commandline_arguments(commandline_arguments, "assume_dependent_codeunits_are_already_built")
        if result is None:
            return default_value
        else:
            return GeneralUtilities.string_to_boolean(result)

    @staticmethod
    @GeneralUtilities.check_arguments
    def get_verbosity_from_commandline_arguments(commandline_arguments: list[str],  default_value: int) -> int:
        result = TasksForCommonProjectStructure.get_property_from_commandline_arguments(commandline_arguments, "verbosity")
        if result is None:
            return default_value
        else:
            return int(result)

    @staticmethod
    @GeneralUtilities.check_arguments
    def get_targetenvironmenttype_from_commandline_arguments(commandline_arguments: list[str],  default_value: str) -> str:
        result = TasksForCommonProjectStructure.get_property_from_commandline_arguments(commandline_arguments, "targetenvironmenttype")
        if result is None:
            return default_value
        else:
            return result

    @staticmethod
    @GeneralUtilities.check_arguments
    def get_additionalargumentsfile_from_commandline_arguments(commandline_arguments: list[str],  default_value: str) -> str:
        result = TasksForCommonProjectStructure.get_property_from_commandline_arguments(commandline_arguments, "additionalargumentsfile")
        if result is None:
            return default_value
        else:
            return result

    @staticmethod
    @GeneralUtilities.check_arguments
    def get_filestosign_from_commandline_arguments(commandline_arguments: list[str],  default_value: dict[str, str]) -> dict[str, str]():
        result_plain = TasksForCommonProjectStructure.get_property_from_commandline_arguments(commandline_arguments, "sign")
        if result_plain is None:
            return default_value
        else:
            result: dict[str, str] = dict[str, str]()
            files_tuples = GeneralUtilities.to_list(result_plain, ";")
            for files_tuple in files_tuples:
                splitted = files_tuple.split("=")
                result[splitted[0]] = splitted[1]
            return result

    @staticmethod
    @GeneralUtilities.check_arguments
    def get_property_from_commandline_arguments(commandline_arguments: list[str], property_name: str) -> str:
        result: str = None
        for commandline_argument in commandline_arguments[1:]:
            prefix = f"--overwrite_{property_name}"
            if commandline_argument.startswith(prefix):
                if m := re.match(f"^{re.escape(prefix)}=(.+)$", commandline_argument):
                    result = m.group(1)
        return result

    @GeneralUtilities.check_arguments
    def update_version_of_codeunit_to_project_version(self, common_tasks_file: str, current_version: str) -> None:
        codeunit_name: str = os.path.basename(GeneralUtilities.resolve_relative_path("..", os.path.dirname(common_tasks_file)))
        codeunit_file: str = os.path.join(GeneralUtilities.resolve_relative_path("..", os.path.dirname(common_tasks_file)), f"{codeunit_name}.codeunit.xml")
        self.write_version_to_codeunit_file(codeunit_file, current_version)

    @GeneralUtilities.check_arguments
    def t4_transform(self, commontasks_script_file_of_current_file: str, verbosity: int):
        sc = ScriptCollectionCore()
        codeunit_folder: str = str(Path(os.path.dirname(commontasks_script_file_of_current_file)).parent.absolute())
        codeunitname: str = os.path.basename(str(Path(os.path.dirname(commontasks_script_file_of_current_file)).parent.absolute()))
        csproj_folder = os.path.join(codeunit_folder, codeunitname)
        for search_result in Path(csproj_folder).glob('**/*.tt'):
            tt_file = str(search_result)
            relative_path_to_tt_file = str(Path(tt_file).relative_to(Path(csproj_folder)))
            sc.run_program("texttransform", relative_path_to_tt_file, csproj_folder, verbosity=verbosity)

    @GeneralUtilities.check_arguments
    def standardized_tasks_generate_reference_by_docfx(self, generate_reference_script_file: str, verbosity: int, targetenvironmenttype: str, commandline_arguments: list[str]) -> None:
        verbosity = TasksForCommonProjectStructure.get_verbosity_from_commandline_arguments(commandline_arguments,  verbosity)
        folder_of_current_file = os.path.dirname(generate_reference_script_file)
        generated_reference_folder = GeneralUtilities.resolve_relative_path("../Artifacts/Reference", folder_of_current_file)
        GeneralUtilities.ensure_directory_does_not_exist(generated_reference_folder)
        GeneralUtilities.ensure_directory_exists(generated_reference_folder)
        obj_folder = os.path.join(folder_of_current_file, "obj")
        GeneralUtilities.ensure_directory_does_not_exist(obj_folder)
        GeneralUtilities.ensure_directory_exists(obj_folder)
        self.__sc.run_program("docfx", "docfx.json", folder_of_current_file, verbosity=verbosity)
        GeneralUtilities.ensure_directory_does_not_exist(obj_folder)

    @GeneralUtilities.check_arguments
    def __standardized_tasks_build_for_dotnet_build(self, csproj_file: str, buildconfiguration: str, originaloutputfolder: str, files_to_sign: dict[str, str], commitid: str,
                                                    verbosity: int, runtimes: list[str]):
        for runtime in runtimes:
            outputfolder = originaloutputfolder+runtime
            csproj_file_folder = os.path.dirname(csproj_file)
            csproj_file_name = os.path.basename(csproj_file)
            self.__sc.run_program("dotnet", "clean", csproj_file_folder, verbosity=verbosity)
            GeneralUtilities.ensure_directory_does_not_exist(os.path.join(csproj_file_folder, "bin"))
            GeneralUtilities.ensure_directory_does_not_exist(os.path.join(csproj_file_folder, "obj"))
            GeneralUtilities.ensure_directory_does_not_exist(outputfolder)
            GeneralUtilities.ensure_directory_exists(outputfolder)
            # TODO pass commitid, timestamp and if desired something like keypair, certificate to the src-code
            self.__sc.run_program("dotnet", f"build {csproj_file_name} -c {buildconfiguration} -o {outputfolder} --runtime {runtime}", csproj_file_folder, verbosity=verbosity)
            for file, keyfile in files_to_sign.items():
                self.__sc.dotnet_sign_file(os.path.join(outputfolder, file), keyfile, verbosity)

    @GeneralUtilities.check_arguments
    def standardized_tasks_build_for_dotnet_project(self, buildscript_file: str, default_target_environmenttype: str,
                                                    target_environmenttype_mapping:  dict[str, str], runtimes: list[str], verbosity: int, commandline_arguments: list[str]):
        # hint: arguments can be overwritten by commandline_arguments
        # this function builds an exe or dll
        target_environmenttype = self.get_targetenvironmenttype_from_commandline_arguments(commandline_arguments, default_target_environmenttype)
        self.__standardized_tasks_build_for_dotnet_project(
            buildscript_file, target_environmenttype_mapping, default_target_environmenttype, verbosity, target_environmenttype, runtimes, commandline_arguments)

    @GeneralUtilities.check_arguments
    def standardized_tasks_build_for_dotnet_library_project(self, buildscript_file: str, default_target_environmenttype: str,
                                                            target_environmenttype_mapping:  dict[str, str], runtimes: list[str],
                                                            verbosity: int, commandline_arguments: list[str]):
        # hint: arguments can be overwritten by commandline_arguments
        # this function builds an exe or dll and converts it to a nupkg-file
        target_environmenttype = self.get_targetenvironmenttype_from_commandline_arguments(commandline_arguments, default_target_environmenttype)
        self.__standardized_tasks_build_for_dotnet_project(
            buildscript_file, target_environmenttype_mapping, default_target_environmenttype, verbosity, target_environmenttype, runtimes, commandline_arguments)
        self.__standardized_tasks_build_nupkg_for_dotnet_create_package(buildscript_file, verbosity, commandline_arguments)

    @GeneralUtilities.check_arguments
    def __get_dotnet_buildconfiguration_by_target_environmenttype(self, targetenvironmenttype: str, default_value: str, commandline_arguments: list[str]):
        if targetenvironmenttype == TasksForCommonProjectStructure.get_development_environment_name():
            return self.get_buildconfigurationdevelopment_from_commandline_arguments(commandline_arguments, default_value)
        if targetenvironmenttype == TasksForCommonProjectStructure.get_qualitycheck_environment_name():
            return self.get_buildconfigurationqualitycheck_from_commandline_arguments(commandline_arguments, default_value)
        if targetenvironmenttype == TasksForCommonProjectStructure.get_productive_environment_name():
            return self.get_buildconfigurationproductive_from_commandline_arguments(commandline_arguments,  "Release")
        raise ValueError(f"Unknown build-environmenttype: {targetenvironmenttype}")

    @GeneralUtilities.check_arguments
    def get_default_target_environmenttype_mapping(self) -> dict[str, str]:
        return {
            TasksForCommonProjectStructure.get_development_environment_name(): TasksForCommonProjectStructure.get_development_environment_name(),
            TasksForCommonProjectStructure.get_qualitycheck_environment_name(): TasksForCommonProjectStructure.get_qualitycheck_environment_name(),
            TasksForCommonProjectStructure.get_productive_environment_name(): TasksForCommonProjectStructure.get_productive_environment_name()
        }

    @GeneralUtilities.check_arguments
    def __standardized_tasks_build_for_dotnet_project(self, buildscript_file: str, target_environmenttype_mapping:  dict[str, str],
                                                      default_build_configuration: str,  verbosity: int, target_environmenttype: str,
                                                      runtimes: list[str], commandline_arguments: list[str]):
        dotnet_build_configuration: str = target_environmenttype_mapping[target_environmenttype]
        codeunitname: str = os.path.basename(str(Path(os.path.dirname(buildscript_file)).parent.parent.absolute()))
        verbosity = TasksForCommonProjectStructure.get_verbosity_from_commandline_arguments(commandline_arguments,  verbosity)
        files_to_sign: dict[str, str] = TasksForCommonProjectStructure.get_filestosign_from_commandline_arguments(commandline_arguments,  dict())
        repository_folder: str = str(Path(os.path.dirname(buildscript_file)).parent.parent.parent.absolute())
        commitid = self.__sc.git_get_commit_id(repository_folder)
        outputfolder = GeneralUtilities.resolve_relative_path("../Artifacts", os.path.dirname(buildscript_file))
        codeunit_folder = os.path.join(repository_folder, codeunitname)
        csproj_file = os.path.join(codeunit_folder, codeunitname, codeunitname+".csproj")
        csproj_test_file = os.path.join(codeunit_folder, codeunitname+"Tests", codeunitname+"Tests.csproj")
        buildconfiguration = self.__get_dotnet_buildconfiguration_by_target_environmenttype(dotnet_build_configuration, default_build_configuration, commandline_arguments)

        self.__sc.run_program("dotnet", "restore", codeunit_folder, verbosity=verbosity)
        self.__standardized_tasks_build_for_dotnet_build(csproj_file, buildconfiguration,
                                                         os.path.join(outputfolder, "BuildResult_DotNet_"), files_to_sign, commitid, verbosity, runtimes)
        self.__standardized_tasks_build_for_dotnet_build(csproj_test_file, buildconfiguration,
                                                         os.path.join(outputfolder, "BuildResult_DotNetTests_"), files_to_sign, commitid, verbosity, runtimes)
        self.generate_sbom_for_dotnet_project(codeunit_folder, verbosity, commandline_arguments)

    @GeneralUtilities.check_arguments
    def __standardized_tasks_build_nupkg_for_dotnet_create_package(self, buildscript_file: str, verbosity: int, commandline_arguments: list[str]):
        codeunitname: str = os.path.basename(str(Path(os.path.dirname(buildscript_file)).parent.parent.absolute()))
        verbosity = TasksForCommonProjectStructure.get_verbosity_from_commandline_arguments(commandline_arguments,  verbosity)
        repository_folder: str = str(Path(os.path.dirname(buildscript_file)).parent.parent.parent.absolute())
        build_folder = os.path.join(repository_folder, codeunitname, "Other", "Build")
        outputfolder = GeneralUtilities.resolve_relative_path("../Artifacts/BuildResult_NuGet", os.path.dirname(buildscript_file))
        root: etree._ElementTree = etree.parse(os.path.join(build_folder, f"{codeunitname}.nuspec"))
        current_version = root.xpath("//*[name() = 'package']/*[name() = 'metadata']/*[name() = 'version']/text()")[0]
        nupkg_filename = f"{codeunitname}.{current_version}.nupkg"
        nupkg_file = f"{build_folder}/{nupkg_filename}"
        GeneralUtilities.ensure_file_does_not_exist(nupkg_file)
        commit_id = self.__sc.git_get_commit_id(repository_folder)
        self.__sc.run_program("nuget", f"pack {codeunitname}.nuspec -Properties \"commitid={commit_id}\"", build_folder, verbosity=verbosity)
        GeneralUtilities.ensure_directory_does_not_exist(outputfolder)
        GeneralUtilities.ensure_directory_exists(outputfolder)
        os.rename(nupkg_file, f"{outputfolder}/{nupkg_filename}")

    @GeneralUtilities.check_arguments
    def generate_sbom_for_dotnet_project(self, codeunit_folder: str, verbosity: int, commandline_arguments: list[str]) -> None:
        codeunit_name = os.path.basename(codeunit_folder)
        sc = ScriptCollectionCore()
        bomfile_folder = "Other\\Artifacts\\BOM"
        verbosity = TasksForCommonProjectStructure.get_verbosity_from_commandline_arguments(commandline_arguments, verbosity)
        sc.run_program("dotnet", f"CycloneDX {codeunit_name}\\{codeunit_name}.csproj -o {bomfile_folder}", codeunit_folder, verbosity=verbosity)
        codeunitversion = self.get_version_of_codeunit(os.path.join(codeunit_folder, f"{codeunit_name}.codeunit.xml"))
        target = f"{codeunit_folder}\\{bomfile_folder}\\{codeunit_name}.{codeunitversion}.sbom.xml"
        GeneralUtilities.ensure_file_does_not_exist(target)
        os.rename(f"{codeunit_folder}\\{bomfile_folder}\\bom.xml", target)

    @GeneralUtilities.check_arguments
    def standardized_tasks_linting_for_python_codeunit(self, linting_script_file: str, verbosity: int, targetenvironmenttype: str, commandline_arguments: list[str]):
        codeunitname: str = Path(os.path.dirname(linting_script_file)).parent.parent.name
        verbosity = TasksForCommonProjectStructure.get_verbosity_from_commandline_arguments(commandline_arguments,  verbosity)
        repository_folder: str = str(Path(os.path.dirname(linting_script_file)).parent.parent.parent.absolute())
        errors_found = False
        GeneralUtilities.write_message_to_stdout(f"Check for linting-issues in codeunit {codeunitname}.")
        src_folder = os.path.join(repository_folder, codeunitname, codeunitname)
        tests_folder = src_folder+"Tests"
        for file in GeneralUtilities.get_all_files_of_folder(src_folder)+GeneralUtilities.get_all_files_of_folder(tests_folder):
            relative_file_path_in_repository = os.path.relpath(file, repository_folder)
            if file.endswith(".py") and os.path.getsize(file) > 0 and not self.__sc.file_is_git_ignored(relative_file_path_in_repository, repository_folder):
                GeneralUtilities.write_message_to_stdout(f"Check for linting-issues in {os.path.relpath(file,os.path.join(repository_folder,codeunitname))}.")
                linting_result = self.__sc.python_file_has_errors(file, repository_folder)
                if (linting_result[0]):
                    errors_found = True
                    for error in linting_result[1]:
                        GeneralUtilities.write_message_to_stderr(error)
        if errors_found:
            raise Exception("Linting-issues occurred.")
        else:
            GeneralUtilities.write_message_to_stdout("No linting-issues found.")

    @GeneralUtilities.check_arguments
    def standardized_tasks_generate_coverage_report(self, repository_folder: str, codeunitname: str, verbosity: int, generate_badges: bool, targetenvironmenttype: str,
                                                    commandline_arguments: list[str], add_testcoverage_history_entry: bool = None):
        """This script expects that the file '<repositorybasefolder>/<codeunitname>/Other/Artifacts/TestCoverage/TestCoverage.xml'
        which contains a test-coverage-report in the cobertura-format exists.
        This script expectes that the testcoverage-reportfolder is '<repositorybasefolder>/<codeunitname>/Other/Artifacts/TestCoverageReport'.
        This script expectes that a test-coverage-badges should be added to '<repositorybasefolder>/<codeunitname>/Other/Resources/Badges'."""
        codeunit_version = self.get_version_of_codeunit(os.path.join(repository_folder, codeunitname, f"{codeunitname}.codeunit.xml"))
        verbosity = TasksForCommonProjectStructure.get_verbosity_from_commandline_arguments(commandline_arguments, verbosity)
        if verbosity == 0:
            verbose_argument_for_reportgenerator = "Off"
        if verbosity == 1:
            verbose_argument_for_reportgenerator = "Error"
        if verbosity == 2:
            verbose_argument_for_reportgenerator = "Info"
        if verbosity == 3:
            verbose_argument_for_reportgenerator = "Verbose"

        # Generating report
        GeneralUtilities.ensure_directory_does_not_exist(os.path.join(repository_folder, codeunitname, f"{codeunitname}/Other/Artifacts/TestCoverageReport"))
        GeneralUtilities.ensure_directory_exists(os.path.join(repository_folder, codeunitname, "Other/Artifacts/TestCoverageReport"))

        if add_testcoverage_history_entry is None:
            add_testcoverage_history_entry = self.get_is_pre_merge_value_from_commandline_arguments(commandline_arguments, add_testcoverage_history_entry)

        history_argument = ""
        if add_testcoverage_history_entry:
            history_folder = f"{codeunitname}/Other/Resources/TestCoverageHistory"
            GeneralUtilities.ensure_directory_exists(os.path.join(repository_folder, codeunitname, history_folder))
            history_argument = f" -historydir:{history_folder}"
        self.__sc.run_program("reportgenerator", f"-reports:{codeunitname}/Other/Artifacts/TestCoverage/TestCoverage.xml " +
                              f"-targetdir:{codeunitname}/Other/Artifacts/TestCoverageReport --verbosity:{verbose_argument_for_reportgenerator}{history_argument} " +
                              f"-title:{codeunitname} -tag:v{codeunit_version}",
                              repository_folder, verbosity=verbosity)

        # Generating badges
        if generate_badges:
            testcoverageubfolger = "Other/Resources/TestCoverageBadges"
            fulltestcoverageubfolger = os.path.join(repository_folder, codeunitname, testcoverageubfolger)
            GeneralUtilities.ensure_directory_does_not_exist(fulltestcoverageubfolger)
            GeneralUtilities.ensure_directory_exists(fulltestcoverageubfolger)
            self.__sc.run_program("reportgenerator", "-reports:Other/Artifacts/TestCoverage/TestCoverage.xml " +
                                  f"-targetdir:{testcoverageubfolger} -reporttypes:Badges " +
                                  f"--verbosity:{verbose_argument_for_reportgenerator}", os.path.join(repository_folder, codeunitname),
                                  verbosity=verbosity)

    @GeneralUtilities.check_arguments
    def standardized_tasks_run_testcases_for_dotnet_project(self, runtestcases_file: str, targetenvironmenttype: str, verbosity: int, generate_badges: bool,
                                                            commandline_arguments: list[str]):
        codeunit_name: str = os.path.basename(str(Path(os.path.dirname(runtestcases_file)).parent.parent.absolute()))
        verbosity = TasksForCommonProjectStructure.get_verbosity_from_commandline_arguments(commandline_arguments,  verbosity)
        repository_folder: str = str(Path(os.path.dirname(runtestcases_file)).parent.parent.parent.absolute())
        testprojectname = codeunit_name+"Tests"
        coverage_file_folder = os.path.join(repository_folder, codeunit_name, "Other/Artifacts/TestCoverage")
        coveragefiletarget = os.path.join(coverage_file_folder,  "TestCoverage.xml")
        buildconfiguration = self.__get_dotnet_buildconfiguration_by_target_environmenttype(targetenvironmenttype, codeunit_name, commandline_arguments)
        with tempfile.TemporaryDirectory() as temp_directory:
            self.__sc.run_program_argsasarray("dotnet", ["test", f"{testprojectname}/{testprojectname}.csproj", "-c", buildconfiguration,
                                                         "--verbosity", "normal", "--collect", "XPlat Code Coverage", "--results-directory", temp_directory],
                                              os.path.join(repository_folder, codeunit_name), verbosity=verbosity)
            temp_directory_subdir = GeneralUtilities.get_direct_folders_of_folder(temp_directory)[0]
            test_coverage_file = GeneralUtilities.get_direct_files_of_folder(temp_directory_subdir)[0]
            GeneralUtilities.ensure_directory_exists(coverage_file_folder)
            GeneralUtilities.ensure_file_does_not_exist(coveragefiletarget)
            shutil.copy(test_coverage_file, coveragefiletarget)
        self.run_testcases_common_post_task(repository_folder, codeunit_name, verbosity, generate_badges, targetenvironmenttype, commandline_arguments)

    def run_testcases_common_post_task(self, repository_folder: str, codeunit_name: str, verbosity: int, generate_badges: bool,
                                       targetenvironmenttype: str, commandline_arguments: list[str]):
        coverage_file_folder = os.path.join(repository_folder, codeunit_name, "Other/Artifacts/TestCoverage")
        coveragefiletarget = os.path.join(coverage_file_folder,  "TestCoverage.xml")
        self.update_path_of_source(repository_folder, codeunit_name)
        self.standardized_tasks_generate_coverage_report(repository_folder, codeunit_name, verbosity, generate_badges, targetenvironmenttype, commandline_arguments)
        self.check_testcoverage(coveragefiletarget, repository_folder, codeunit_name)

    @GeneralUtilities.check_arguments
    def write_version_to_codeunit_file(self, codeunit_file: str, current_version: str) -> None:
        versionregex = "\\d+\\.\\d+\\.\\d+"
        versiononlyregex = f"^{versionregex}$"
        pattern = re.compile(versiononlyregex)
        if pattern.match(current_version):
            GeneralUtilities.write_text_to_file(codeunit_file, re.sub(f"<cps:version>{versionregex}<\\/cps:version>",
                                                                      f"<cps:version>{current_version}</cps:version>", GeneralUtilities.read_text_from_file(codeunit_file)))
        else:
            raise ValueError(f"Version '{current_version}' does not match version-regex '{versiononlyregex}'.")

    @GeneralUtilities.check_arguments
    def standardized_tasks_linting_for_dotnet_project(self, linting_script_file: str, verbosity: int, targetenvironmenttype: str, commandline_arguments: list[str]):
        verbosity = TasksForCommonProjectStructure.get_verbosity_from_commandline_arguments(commandline_arguments,  verbosity)
        # TODO implement function

    @GeneralUtilities.check_arguments
    def __export_codeunit_reference_content_to_reference_repository(self, project_version_identifier: str, replace_existing_content: bool, target_folder_for_reference_repository: str,
                                                                    repository: str, codeunitname, projectname: str, codeunit_version: str, public_repository_url: str, branch: str) -> None:
        target_folder = os.path.join(target_folder_for_reference_repository, project_version_identifier, codeunitname)
        if os.path.isdir(target_folder) and not replace_existing_content:
            raise ValueError(f"Folder '{target_folder}' already exists.")
        GeneralUtilities.ensure_directory_does_not_exist(target_folder)
        GeneralUtilities.ensure_directory_exists(target_folder)
        codeunit_version_identifier = "Latest" if project_version_identifier == "Latest" else "v"+codeunit_version
        title = f"Reference of codeunit {codeunitname} <i>{codeunit_version_identifier}</i> (contained in project {projectname} <i>{project_version_identifier}</i>)"
        if public_repository_url is None:
            repo_url_html = ""
        else:
            repo_url_html = f'<a href="{public_repository_url}/tree/{branch}/{codeunitname}">Source-code</a>'
        index_file_for_reference = os.path.join(target_folder, "index.html")
        index_file_content = f"""<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8">
    <title>{title}</title>
  </head>
  <body>
    <h1 class="display-1">{title}</h1>
    <hr/>
    Available reference-content for {codeunitname}:<br>
    {repo_url_html}<br>
    <a href="./Reference/index.html">Reference</a><br>
    <a href="./TestCoverageReport/index.html">TestCoverageReport</a><br>
  </body>
</html>
"""  # see https://getbootstrap.com/docs/5.1/getting-started/introduction/
        GeneralUtilities.ensure_file_exists(index_file_for_reference)
        GeneralUtilities.write_text_to_file(index_file_for_reference, index_file_content)
        other_folder_in_repository = os.path.join(repository, codeunitname, "Other")
        source_generatedreference = os.path.join(other_folder_in_repository, "Artifacts", "Reference")
        target_generatedreference = os.path.join(target_folder, "Reference")
        shutil.copytree(source_generatedreference, target_generatedreference)
        source_testcoveragereport = os.path.join(other_folder_in_repository, "Artifacts", "TestCoverageReport")
        target_testcoveragereport = os.path.join(target_folder, "TestCoverageReport")
        shutil.copytree(source_testcoveragereport, target_testcoveragereport)

    @GeneralUtilities.check_arguments
    def __standardized_tasks_release_buildartifact(self, information: CreateReleaseInformationForProjectInCommonProjectFormat) -> None:
        # This function is intended to be called directly after __standardized_tasks_merge_to_stable_branch
        project_version = self.__sc.get_semver_version_from_gitversion(information.repository)
        target_folder_base = os.path.join(information.artifacts_folder, information.projectname, project_version)
        GeneralUtilities.ensure_directory_exists(target_folder_base)

        self.build_codeunits(information.repository, information.verbosity, information.target_environmenttype_for_productive,
                             information.additional_arguments_file, False, information.export_target)

        reference_folder = os.path.join(information.reference_repository, "ReferenceContent")

        for codeunitname in self.get_codeunits(information.repository):

            # Push artifacts to registry
            scriptfilename = f"PushBuildArtifacts.{codeunitname}.py"
            push_artifact_to_registry_script = os.path.join(information.push_artifacts_scripts_folder, scriptfilename)
            if os.path.isfile(push_artifact_to_registry_script):
                GeneralUtilities.write_message_to_stdout(f"Push buildartifact of codeunit {codeunitname}.")
                self.__sc.run_program("python", push_artifact_to_registry_script, information.push_artifacts_scripts_folder,
                                      verbosity=information.verbosity, throw_exception_if_exitcode_is_not_zero=True)

            codeunit_version = self.get_version_of_codeunit_folder(os.path.join(information.repository, codeunitname))

            # Copy reference of codeunit to reference-repository
            self.__export_codeunit_reference_content_to_reference_repository(f"v{project_version}", False, reference_folder, information.repository,
                                                                             codeunitname, information.projectname, codeunit_version, information.public_repository_url,
                                                                             f"v{project_version}")
            self.__export_codeunit_reference_content_to_reference_repository("Latest", True, reference_folder, information.repository,
                                                                             codeunitname, information.projectname, codeunit_version, information.public_repository_url,
                                                                             information.target_branch_name)

            # Generate reference
            self.__generate_entire_reference(information.projectname, project_version, reference_folder)

    @GeneralUtilities.check_arguments
    def __generate_entire_reference(self, projectname: str, project_version: str, reference_folder: str) -> None:
        all_available_version_identifier_folders_of_reference = list(
            folder for folder in GeneralUtilities.get_direct_folders_of_folder(reference_folder))
        all_available_version_identifier_folders_of_reference.reverse()  # move newer versions above
        all_available_version_identifier_folders_of_reference.insert(0, all_available_version_identifier_folders_of_reference.pop())  # move latest version to the top
        reference_versions_html_lines = []
        for all_available_version_identifier_folder_of_reference in all_available_version_identifier_folders_of_reference:
            version_identifier_of_project = os.path.basename(all_available_version_identifier_folder_of_reference)
            if version_identifier_of_project == "Latest":
                latest_version_hint = f" (v {project_version})"
            else:
                latest_version_hint = ""
            reference_versions_html_lines.append('    <hr/>')
            reference_versions_html_lines.append(f'    <h2 class="display-2">{version_identifier_of_project}{latest_version_hint}</h2>')
            reference_versions_html_lines.append("    Contained codeunits:<br/>")
            reference_versions_html_lines.append("    <ul>")
            for codeunit_reference_folder in list(folder for folder in GeneralUtilities.get_direct_folders_of_folder(all_available_version_identifier_folder_of_reference)):
                reference_versions_html_lines.append(f'      <li><a href="./{version_identifier_of_project}/{os.path.basename(codeunit_reference_folder)}/index.html">' +
                                                     f'{os.path.basename(codeunit_reference_folder)} {version_identifier_of_project}</a></li>')
            reference_versions_html_lines.append("    </ul>")

        reference_versions_links_file_content = "    \n".join(reference_versions_html_lines)
        title = f"{projectname}-reference"
        reference_index_file = os.path.join(reference_folder, "index.html")
        reference_index_file_content = f"""<!DOCTYPE html>
<html lang="en">

  <head>
    <meta charset="UTF-8">
    <title>{title}</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.2.2/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-1BmE4kWBq78iYhFldvKuhfTAU6auU8tT94WrHftjDbrCEXSU1oBoqyl2QvZ6jIW3" crossorigin="anonymous">
  </head>

  <body>
    <h1 class="display-1">{title}</h1>
    <hr/>
{reference_versions_links_file_content}
  </body>

</html>
"""  # see https://getbootstrap.com/docs/5.1/getting-started/introduction/
        GeneralUtilities.write_text_to_file(reference_index_file, reference_index_file_content)

    @GeneralUtilities.check_arguments
    def push_nuget_build_artifact(self, push_script_file: str, codeunitname: str, registry_address: str, api_key: str):
        # when pusing to "default public" nuget-server then use registry_address: "nuget.org"
        build_artifact_folder = GeneralUtilities.resolve_relative_path(
            f"../../Submodules/{codeunitname}/{codeunitname}/Other/Artifacts/BuildResult_NuGet", os.path.dirname(push_script_file))
        self.__sc.push_nuget_build_artifact(self.__sc.find_file_by_extension(build_artifact_folder, "nupkg"),
                                            registry_address, api_key)

    @GeneralUtilities.check_arguments
    def assert_no_uncommitted_changes(self, repository_folder: str):
        if self.__sc.git_repository_has_uncommitted_changes(repository_folder):
            raise ValueError(f"Repository '{repository_folder}' has uncommitted changes.")

    @GeneralUtilities.check_arguments
    def get_codeunits(self, repository_folder: str) -> list[str]:
        result: list[str] = []
        for direct_subfolder in GeneralUtilities.get_direct_folders_of_folder(repository_folder):
            subfoldername = os.path.basename(direct_subfolder)
            if os.path.isfile(os.path.join(direct_subfolder, f"{subfoldername}.codeunit.xml")):
                result.append(subfoldername)
        return result

    @GeneralUtilities.check_arguments
    def merge_to_main_branch(self, repository_folder: str, source_branch: str = "other/next-release",
                             target_branch: str = "main", verbosity: int = 1, additional_arguments_file: str = None, fast_forward_source_branch: bool = False) -> None:
        # This is an automatization for 1-man-projects. Usual this merge would be done by a pull request in a sourcecode-version-control-platform
        # (like GitHub, GitLab or Azure DevOps)
        self.assert_no_uncommitted_changes(repository_folder)
        self.__sc.git_checkout(repository_folder, source_branch)
        self.build_codeunits(repository_folder, verbosity, "QualityCheck", additional_arguments_file, True, None)
        self.__sc.git_merge(repository_folder, source_branch, target_branch, False, False, None)
        self.__sc.git_commit(repository_folder, f'Merge branch {source_branch} into {target_branch}', stage_all_changes=True, no_changes_behavior=1)
        self.__sc.git_checkout(repository_folder, target_branch)
        if fast_forward_source_branch:
            self.__sc.git_merge(repository_folder, target_branch, source_branch, True, True)

    @GeneralUtilities.check_arguments
    def merge_to_stable_branch(self, create_release_file: str, createRelease_configuration: CreateReleaseConfiguration):

        GeneralUtilities.write_message_to_stdout(f"Create release for project {createRelease_configuration.projectname}.")
        folder_of_create_release_file_file = os.path.abspath(os.path.dirname(create_release_file))

        build_repository_folder = GeneralUtilities.resolve_relative_path(f"..{os.path.sep}..", folder_of_create_release_file_file)
        self.assert_no_uncommitted_changes(build_repository_folder)

        self.__sc.git_checkout(build_repository_folder, createRelease_configuration.build_repository_branch)

        repository_folder = GeneralUtilities.resolve_relative_path(f"Submodules{os.path.sep}{createRelease_configuration.projectname}", build_repository_folder)
        mergeInformation = MergeToStableBranchInformationForProjectInCommonProjectFormat(repository_folder,
                                                                                         createRelease_configuration.additional_arguments_file,
                                                                                         createRelease_configuration.artifacts_folder)
        mergeInformation.verbosity = createRelease_configuration.verbosity
        mergeInformation.push_target_branch = createRelease_configuration.remotename is not None
        mergeInformation.push_target_branch_remote_name = createRelease_configuration.remotename
        mergeInformation.push_source_branch = createRelease_configuration.remotename is not None
        mergeInformation.push_source_branch_remote_name = createRelease_configuration.remotename
        new_project_version = self.__standardized_tasks_merge_to_stable_branch(mergeInformation)

        createReleaseInformation = CreateReleaseInformationForProjectInCommonProjectFormat(repository_folder,
                                                                                           createRelease_configuration.artifacts_folder,
                                                                                           createRelease_configuration.projectname,
                                                                                           createRelease_configuration.public_repository_url,
                                                                                           mergeInformation.targetbranch,
                                                                                           mergeInformation.additional_arguments_file,
                                                                                           mergeInformation.export_target,
                                                                                           createRelease_configuration.push_artifacts_scripts_folder)
        createReleaseInformation.verbosity = createRelease_configuration.verbosity
        self.__standardized_tasks_release_buildartifact(createReleaseInformation)

        self.__sc.git_commit(createReleaseInformation.reference_repository, f"Added reference of {createRelease_configuration.projectname} v{new_project_version}")
        if createRelease_configuration.reference_repository_remote_name is not None:
            self.__sc.git_push(createReleaseInformation.reference_repository, createRelease_configuration.reference_repository_remote_name,
                               createRelease_configuration.reference_repository_branch_name, createRelease_configuration.reference_repository_branch_name,
                               verbosity=createRelease_configuration.verbosity)
        self.__sc.git_commit(build_repository_folder, f"Added {createRelease_configuration.projectname} release v{new_project_version}")
        GeneralUtilities.write_message_to_stdout(f"Finished release for project {createRelease_configuration.projectname} successfully.")
        return new_project_version

    @GeneralUtilities.check_arguments
    def create_release_starter_for_repository_in_standardized_format(self, create_release_file: str, logfile: str, verbosity: int, addLogOverhead: bool,
                                                                     commandline_arguments: list[str]):
        # hint: arguments can be overwritten by commandline_arguments
        folder_of_this_file = os.path.dirname(create_release_file)
        verbosity = TasksForCommonProjectStructure.get_verbosity_from_commandline_arguments(commandline_arguments, verbosity)
        self.__sc.run_program("python", f"CreateRelease.py --overwrite_verbosity={str(verbosity)}",
                              folder_of_this_file,  verbosity=verbosity, log_file=logfile, addLogOverhead=addLogOverhead)

    @GeneralUtilities.check_arguments
    def __standardized_tasks_merge_to_stable_branch(self, information: MergeToStableBranchInformationForProjectInCommonProjectFormat) -> str:

        src_branch_commit_id = self.__sc.git_get_commit_id(information.repository,  information.sourcebranch)
        if (src_branch_commit_id == self.__sc.git_get_commit_id(information.repository,  information.targetbranch)):
            GeneralUtilities.write_message_to_stderr(
                f"Can not merge because the source-branch and the target-branch are on the same commit (commit-id: {src_branch_commit_id})")

        self.assert_no_uncommitted_changes(information.repository)
        self.__sc.git_checkout(information.repository, information.sourcebranch)
        self.__sc.run_program("git", "clean -dfx", information.repository,  verbosity=information.verbosity, throw_exception_if_exitcode_is_not_zero=True)
        project_version = self.__sc.get_semver_version_from_gitversion(information.repository)

        self.build_codeunits(information.repository, information.verbosity, information.target_environmenttype_for_qualitycheck,
                             information.additional_arguments_file, False, information.export_target)

        self.assert_no_uncommitted_changes(information.repository)

        commit_id = self.__sc.git_merge(information.repository, information.sourcebranch, information.targetbranch, True, True)
        self.__sc.git_create_tag(information.repository, commit_id, f"v{project_version}", information.sign_git_tags)

        if information.push_source_branch:
            GeneralUtilities.write_message_to_stdout("Push source-branch...")
            self.__sc.git_push(information.repository, information.push_source_branch_remote_name,
                               information.sourcebranch, information.sourcebranch, pushalltags=True, verbosity=information.verbosity)

        if information.push_target_branch:
            GeneralUtilities.write_message_to_stdout("Push target-branch...")
            self.__sc.git_push(information.repository, information.push_target_branch_remote_name,
                               information.targetbranch, information.targetbranch, pushalltags=True, verbosity=information.verbosity)

        return project_version

    @GeneralUtilities.check_arguments
    def standardized_tasks_build_for_docker_project(self, build_script_file: str, target_environment_type: str,
                                                    verbosity: int, commandline_arguments: list[str]):
        use_cache: bool = target_environment_type != "Productive"
        verbosity = TasksForCommonProjectStructure.get_verbosity_from_commandline_arguments(commandline_arguments, verbosity)
        sc: ScriptCollectionCore = ScriptCollectionCore()
        codeunitname: str = Path(os.path.dirname(build_script_file)).parent.parent.name
        codeunit_folder = GeneralUtilities.resolve_relative_path("../..", str(os.path.dirname(build_script_file)))
        codeunitname_lower = codeunitname.lower()
        codeunitversion = self.get_version_of_codeunit(os.path.join(codeunit_folder, f"{codeunitname}.codeunit.xml"))
        args = ["image", "build", "--pull", "--force-rm", "--progress=plain", "--build-arg", f"TargetEnvironmentType={target_environment_type}",
                "--tag", f"{codeunitname_lower}:latest", "--tag", f"{codeunitname_lower}:{codeunitversion}", "--file", f"{codeunitname}/Dockerfile"]
        if not use_cache:
            args.append("--no-cache")
        args.append(".")
        codeunit_content_folder = os.path.join(codeunit_folder)
        sc.run_program_argsasarray("docker", args, codeunit_content_folder, verbosity=verbosity, print_errors_as_information=True)
        artifacts_folder = GeneralUtilities.resolve_relative_path("Other/Artifacts", codeunit_folder)
        app_artifacts_folder = os.path.join(artifacts_folder, "BuildResult_OCIImage")
        GeneralUtilities.ensure_directory_does_not_exist(app_artifacts_folder)
        GeneralUtilities.ensure_directory_exists(app_artifacts_folder)
        self.__sc.run_program_argsasarray("docker", ["save", "--output", f"{codeunitname}_v{codeunitversion}.tar",
                                                     f"{codeunitname_lower}:{codeunitversion}"], app_artifacts_folder,
                                          verbosity=verbosity, print_errors_as_information=True)

    @GeneralUtilities.check_arguments
    def generate_sbom_for_docker_image(self, build_script_file: str, verbosity: int, commandline_arguments: list[str]) -> None:
        verbosity = TasksForCommonProjectStructure.get_verbosity_from_commandline_arguments(commandline_arguments, verbosity)
        codeunitname: str = Path(os.path.dirname(build_script_file)).parent.parent.name
        codeunit_folder = GeneralUtilities.resolve_relative_path("../..", str(os.path.dirname(build_script_file)))
        artifacts_folder = GeneralUtilities.resolve_relative_path("Other/Artifacts", codeunit_folder)
        codeunitname_lower = codeunitname.lower()
        sbom_folder = os.path.join(artifacts_folder, "BOM")
        codeunitversion = self.get_version_of_codeunit(os.path.join(codeunit_folder, f"{codeunitname}.codeunit.xml"))
        GeneralUtilities.ensure_directory_exists(sbom_folder)
        self.__sc.run_program_argsasarray("docker", ["sbom", "--format", "cyclonedx", f"{codeunitname_lower}:{codeunitversion}",
                                                     "--output", f"{codeunitname}.{codeunitversion}.sbom.xml"], sbom_folder, verbosity=verbosity, print_errors_as_information=True)

    @GeneralUtilities.check_arguments
    def push_docker_build_artifact(self, push_artifacts_file: str, registry: str, product_name: str, codeunitname: str,
                                   verbosity: int, push_readme: bool, commandline_arguments: list[str]):
        folder_of_this_file = os.path.dirname(push_artifacts_file)
        verbosity = TasksForCommonProjectStructure.get_verbosity_from_commandline_arguments(commandline_arguments, verbosity)
        repository_folder = GeneralUtilities.resolve_relative_path(f"..{os.path.sep}..{os.path.sep}Submodules{os.path.sep}{product_name}", folder_of_this_file)
        codeunit_folder = os.path.join(repository_folder, codeunitname)
        artifacts_folder = self.get_artifacts_folder(repository_folder, codeunitname)
        applicationimage_folder = os.path.join(artifacts_folder, "BuildResult_OCIImage")
        sc = ScriptCollectionCore()
        image_file = sc.find_file_by_extension(applicationimage_folder, "tar")
        image_filename = os.path.basename(image_file)
        version = self.get_version_of_codeunit(os.path.join(codeunit_folder, f"{codeunitname}.codeunit.xml"))
        image_tag_name = codeunitname.lower()
        repo = f"{registry}/{image_tag_name}"
        image_latest = f"{repo}:latest"
        image_version = f"{repo}:{version}"
        GeneralUtilities.write_message_to_stdout("Load image...")
        sc.run_program("docker", f"load --input {image_filename}", applicationimage_folder, verbosity=verbosity)
        GeneralUtilities.write_message_to_stdout("Tag image...")
        sc.run_program("docker", f"tag {image_tag_name}:{version} {image_latest}", verbosity=verbosity)
        sc.run_program("docker", f"tag {image_tag_name}:{version} {image_version}", verbosity=verbosity)
        GeneralUtilities.write_message_to_stdout("Push image...")
        sc.run_program("docker", f"push {image_latest}", verbosity=verbosity)
        sc.run_program("docker", f"push {image_version}", verbosity=verbosity)
        if push_readme:
            sc.run_program("docker", f"pushrm {repo}", codeunit_folder, verbosity=verbosity)

    @GeneralUtilities.check_arguments
    def get_dependent_code_units(self, codeunit_file: str) -> set[str]:
        root: etree._ElementTree = etree.parse(codeunit_file)
        return set(root.xpath('//cps:dependentcodeunit/text()', namespaces={
            'cps': 'https://projects.aniondev.de/PublicProjects/Common/ProjectTemplates/-/tree/main/Conventions/RepositoryStructure/CommonProjectStructure'
        }))

    @GeneralUtilities.check_arguments
    def standardized_tasks_run_testcases_for_docker_project(self, run_testcases_script_file: str, verbosity: int, targetenvironmenttype: str,
                                                            commandline_arguments: list[str], generate_badges: bool = True):
        codeunit_folder = GeneralUtilities.resolve_relative_path("../..", str(os.path.dirname(run_testcases_script_file)))
        repository_folder: str = str(Path(os.path.dirname(run_testcases_script_file)).parent.parent.parent.absolute())
        codeunitname: str = Path(os.path.dirname(run_testcases_script_file)).parent.parent.name
        date = int(round(datetime.now().timestamp()))
        # TODO generate real coverage report
        dummy_test_coverage_file = f"""<?xml version="1.0" ?>
        <coverage version="6.3.2" timestamp="{date}" lines-valid="0" lines-covered="0" line-rate="0" branches-covered="0" branches-valid="0" branch-rate="0" complexity="0">
            <sources>
                <source>{codeunitname}</source>
            </sources>
            <packages>
                <package name="{codeunitname}" line-rate="0" branch-rate="0" complexity="0">
                </package>
            </packages>
        </coverage>"""
        artifacts_folder = GeneralUtilities.resolve_relative_path("Other/Artifacts", codeunit_folder)
        testcoverage_artifacts_folder = os.path.join(artifacts_folder, "TestCoverage")
        GeneralUtilities.ensure_directory_exists(testcoverage_artifacts_folder)
        testcoverage_file = os.path.join(testcoverage_artifacts_folder, "TestCoverage.xml")
        GeneralUtilities.ensure_file_exists(testcoverage_file)
        GeneralUtilities.write_text_to_file(testcoverage_file, dummy_test_coverage_file)
        self.run_testcases_common_post_task(repository_folder, codeunitname, verbosity, generate_badges, targetenvironmenttype, commandline_arguments)

    @GeneralUtilities.check_arguments
    def standardized_tasks_linting_for_docker_project(self, linting_script_file: str, verbosity: int, targetenvironmenttype: str, commandline_arguments: list[str]) -> None:
        verbosity = TasksForCommonProjectStructure.get_verbosity_from_commandline_arguments(commandline_arguments,  verbosity)
        # TODO

    @GeneralUtilities.check_arguments
    def standardized_tasks_do_common_tasks(self, common_tasks_scripts_file: str, version: str, verbosity: int,  targetenvironmenttype: str,  clear_artifacts_folder: bool,
                                           additional_arguments_file: str, assume_dependent_codeunits_are_already_built: bool, commandline_arguments: list[str]) -> None:
        additional_arguments_file = self.get_additionalargumentsfile_from_commandline_arguments(commandline_arguments, additional_arguments_file)
        target_environmenttype = self.get_targetenvironmenttype_from_commandline_arguments(commandline_arguments, targetenvironmenttype)
        assume_dependent_codeunits_are_already_built = self.get_assume_dependent_codeunits_are_already_built_from_commandline_arguments(commandline_arguments,
                                                                                                                                        assume_dependent_codeunits_are_already_built)
        if commandline_arguments is None:
            raise ValueError('The "commandline_arguments"-parameter is not defined.')
        if len(commandline_arguments) == 0:
            raise ValueError('An empty array as argument for the "commandline_arguments"-parameter is not valid.')
        commandline_arguments = commandline_arguments[1:]
        repository_folder: str = str(Path(os.path.dirname(common_tasks_scripts_file)).parent.parent.absolute())
        codeunitname: str = str(os.path.basename(Path(os.path.dirname(common_tasks_scripts_file)).parent.absolute()))
        verbosity = TasksForCommonProjectStructure.get_verbosity_from_commandline_arguments(commandline_arguments, verbosity)

        # Clear previously builded artifacts if desired:
        if clear_artifacts_folder:
            artifacts_folder = os.path.join(repository_folder, codeunitname, "Other", "Artifacts")
            GeneralUtilities.ensure_directory_does_not_exist(artifacts_folder)

        # Check codeunit-conformity
        # TODO check if foldername=="<codeunitname>[.codeunit.xml]"==codeunitname in file
        codeunitfile = os.path.join(repository_folder, codeunitname, f"{codeunitname}.codeunit.xml")
        if not os.path.isfile(codeunitfile):
            raise Exception(f'Codeunitfile "{codeunitfile}" does not exist.')
        # TODO implement usage of self.reference_latest_version_of_xsd_when_generating_xml
        namespaces = {'cps': 'https://projects.aniondev.de/PublicProjects/Common/ProjectTemplates/-/tree/main/Conventions/RepositoryStructure/CommonProjectStructure',
                      'xsi': 'http://www.w3.org/2001/XMLSchema-instance'}
        root: etree._ElementTree = etree.parse(codeunitfile)
        codeunit_file_version = root.xpath('//cps:codeunit/@codeunitspecificationversion',  namespaces=namespaces)[0]
        supported_codeunitspecificationversion = "1.1.0"
        if codeunit_file_version != supported_codeunitspecificationversion:
            raise ValueError(f"ScriptCollection only supports processing codeunits with codeunit-specification-version={supported_codeunitspecificationversion}.")
        schemaLocation = root.xpath('//cps:codeunit/@xsi:schemaLocation',  namespaces=namespaces)[0]
        xmlschema.validate(codeunitfile, schemaLocation)

        # TODO implement cycle-check for dependent codeunits

        # Get artifacts from dependent codeunits
        if assume_dependent_codeunits_are_already_built:
            pass  # TODO do basic checks to verify dependent codeunits are really there and raise exception if not
        else:
            self.build_dependent_code_units(repository_folder, codeunitname, verbosity, target_environmenttype, additional_arguments_file)
        self.copy_artifacts_from_dependent_code_units(repository_folder, codeunitname)

        # Update version
        self.update_version_of_codeunit_to_project_version(common_tasks_scripts_file, version)

        # set default constants
        self.set_default_constants(os.path.join(repository_folder, codeunitname))

        # Check if changelog exists
        changelog_folder = os.path.join(repository_folder, "Other", "Resources", "Changelog")
        changelog_file = os.path.join(changelog_folder, f"v{version}.md")
        if not os.path.isfile(changelog_file):
            raise ValueError(f"Changelog-file '{changelog_file}' does not exist.")

    @GeneralUtilities.check_arguments
    def get_version_of_project(self, repository_folder: str):
        return ScriptCollectionCore().get_semver_version_from_gitversion(repository_folder)

    @GeneralUtilities.check_arguments
    def replace_common_variables_in_nuspec_file(self, codeunit_folder: str):
        codeunit_name = os.path.basename(codeunit_folder)
        version = self.get_version_of_codeunit_folder(codeunit_folder)
        nuspec_file = os.path.join(codeunit_folder, "Other", "Build", f"{codeunit_name}.nuspec")
        self.__sc.replace_version_in_nuspec_file(nuspec_file, version)

    @GeneralUtilities.check_arguments
    def standardized_tasks_build_for_node_project(self, build_script_file: str, build_environment_target_type: str,
                                                  verbosity: int, commandline_arguments: list[str]):
        # TODO use unused parameter
        sc = ScriptCollectionCore()
        verbosity = TasksForCommonProjectStructure.get_verbosity_from_commandline_arguments(commandline_arguments, verbosity)
        sc.program_runner = ProgramRunnerEpew()
        build_script_folder = os.path.dirname(build_script_file)
        codeunit_folder = GeneralUtilities.resolve_relative_path("../..", build_script_folder)
        sc.run_program("npm", "run build", codeunit_folder, verbosity=verbosity)

    @GeneralUtilities.check_arguments
    def standardized_tasks_linting_for_node_project(self, linting_script_file: str, verbosity: int,
                                                    target_environmenttype: str, commandline_arguments: list[str]):
        # TODO use unused parameter
        sc = ScriptCollectionCore()
        verbosity = TasksForCommonProjectStructure.get_verbosity_from_commandline_arguments(commandline_arguments, verbosity)
        sc.program_runner = ProgramRunnerEpew()
        build_script_folder = os.path.dirname(linting_script_file)
        codeunit_folder = GeneralUtilities.resolve_relative_path("../..", build_script_folder)
        sc.run_program("npm", "run lint", codeunit_folder, verbosity=verbosity)

    @GeneralUtilities.check_arguments
    def standardized_tasks_run_testcases_for_node_project(self, runtestcases_script_file: str,
                                                          targetenvironmenttype: str, generate_badges: bool, verbosity: int,
                                                          commandline_arguments: list[str]):
        # TODO use targetenvironmenttype etc.
        sc = ScriptCollectionCore()
        codeunit_name: str = os.path.basename(str(Path(os.path.dirname(runtestcases_script_file)).parent.parent.absolute()))
        verbosity = TasksForCommonProjectStructure.get_verbosity_from_commandline_arguments(commandline_arguments, verbosity)
        sc.program_runner = ProgramRunnerEpew()
        codeunit_folder = GeneralUtilities.resolve_relative_path("../..", os.path.dirname(runtestcases_script_file))
        sc.run_program("npm", "run test", codeunit_folder, verbosity=verbosity)
        coverage_folder = os.path.join(codeunit_folder, "Other", "Artifacts", "TestCoverage")
        target_file = os.path.join(coverage_folder, "TestCoverage.xml")
        GeneralUtilities.ensure_file_does_not_exist(target_file)
        os.rename(os.path.join(coverage_folder, "cobertura-coverage.xml"), target_file)
        repository_folder = GeneralUtilities.resolve_relative_path("..", codeunit_folder)
        self.run_testcases_common_post_task(repository_folder, codeunit_name, verbosity, generate_badges, targetenvironmenttype, commandline_arguments)

    @GeneralUtilities.check_arguments
    def do_npm_install(self, package_json_folder: str, verbosity: int):
        sc = ScriptCollectionCore()
        sc.program_runner = ProgramRunnerEpew()
        sc.run_program("npm", "install", package_json_folder, verbosity=verbosity)

    @GeneralUtilities. check_arguments
    def set_default_constants(self, codeunit_folder: str):
        self.set_constant_for_commitid(codeunit_folder)
        self.set_constant_for_commitdate(codeunit_folder)
        self.set_constant_for_commitname(codeunit_folder)
        self.set_constant_for_commitversion(codeunit_folder)

    @GeneralUtilities. check_arguments
    def set_constant_for_commitid(self, codeunit_folder: str):
        commit_id = self.__sc.git_get_commit_id(codeunit_folder)
        self.set_constant(codeunit_folder, "CommitId", commit_id)

    @GeneralUtilities. check_arguments
    def set_constant_for_commitdate(self, codeunit_folder: str):
        commit_date: datetime = self.__sc.git_get_commit_date(codeunit_folder)
        self.set_constant(codeunit_folder, "CommitDate", GeneralUtilities.datetime_to_string(commit_date))

    @GeneralUtilities. check_arguments
    def set_constant_for_commitname(self, codeunit_folder: str):
        codeunit_name: str = os.path.basename(codeunit_folder)
        self.set_constant(codeunit_folder, "CodeUnitName", codeunit_name)

    @GeneralUtilities. check_arguments
    def set_constant_for_commitversion(self, codeunit_folder: str):
        codeunit_version: str = self.get_version_of_codeunit_folder(codeunit_folder)
        self.set_constant(codeunit_folder, "CodeUnitVersion", codeunit_version)

    @GeneralUtilities. check_arguments
    def set_constant(self, codeunit_folder: str, constantname: str, constant_value: str, documentationsummary: str = None, constants_valuefile: str = None):
        if documentationsummary is None:
            documentationsummary = ""
        constants_folder = os.path.join(codeunit_folder, "Other", "Resources", "Constants")
        GeneralUtilities.ensure_directory_exists(constants_folder)
        constants_metafile = os.path.join(constants_folder, f"{constantname}.constant.xml")
        if constants_valuefile is None:
            constants_valuefile_folder = constants_folder
            constants_valuefile_name = f"{constantname}.value.txt"
            constants_valuefiler_reference = f"./{constants_valuefile_name}"
        else:
            constants_valuefile_folder = os.path.dirname(constants_valuefile)
            constants_valuefile_name = os.path.basename(constants_valuefile)
            constants_valuefiler_reference = os.path.join(constants_valuefile_folder, constants_valuefile_name)

        # TODO implement usage of self.reference_latest_version_of_xsd_when_generating_xml
        GeneralUtilities.write_text_to_file(constants_metafile, f"""<?xml version="1.0" encoding="UTF-8" ?>
<cps:constant xmlns:cps="https://projects.aniondev.de/PublicProjects/Common/ProjectTemplates/-/tree/main/Conventions/RepositoryStructure/CommonProjectStructure" constantspecificationversion="1.1.0"
    xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="https://projects.aniondev.de/PublicProjects/Common/ProjectTemplates/-/raw/main/Conventions/RepositoryStructure/CommonProjectStructure/constant.xsd">
    <cps:name>{constantname}</cps:name>
    <cps:documentationsummary>{documentationsummary}</cps:documentationsummary>
    <cps:path>{constants_valuefiler_reference}</cps:path>
</cps:constant>""")
        # TODO validate generated xml against xsd
        GeneralUtilities.write_text_to_file(os.path.join(constants_valuefile_folder, constants_valuefile_name), constant_value)

    @GeneralUtilities.check_arguments
    def generate_openapi_file(self, buildscript_file: str, runtime: str, swagger_document_name: str,
                              verbosity: int, commandline_arguments: list[str]) -> None:
        codeunitname = os.path.basename(str(Path(os.path.dirname(buildscript_file)).parent.parent.absolute()))
        repository_folder = str(Path(os.path.dirname(buildscript_file)).parent.parent.parent.absolute())
        artifacts_folder = os.path.join(repository_folder, codeunitname, "Other", "Artifacts")
        GeneralUtilities.ensure_directory_exists(os.path.join(artifacts_folder, "APISpecification"))
        verbosity = TasksForCommonProjectStructure.get_verbosity_from_commandline_arguments(commandline_arguments, verbosity)
        version = self.get_version_of_codeunit_folder(os.path.join(repository_folder, codeunitname))
        self.__sc.run_program("swagger",
                              f"tofile --output APISpecification\\{codeunitname}.v{version}.api.json" +
                              f" BuildResult_DotNet_{runtime}\\{codeunitname}.dll {swagger_document_name}",
                              artifacts_folder, verbosity=verbosity)

    @GeneralUtilities.check_arguments
    def replace_version_in_package_file(self: ScriptCollectionCore, package_json_file: str, version: str):
        filename = package_json_file
        with open(filename, 'r', encoding="utf-8") as f:
            data = json.load(f)
            data['version'] = version
        os.remove(filename)
        with open(filename, 'w', encoding="utf-8") as f:
            json.dump(data, f, indent=2)

    @GeneralUtilities.check_arguments
    def build_dependent_code_units(self, repo_folder: str, codeunit_name: str, verbosity: int, target_environmenttype: str,
                                   additional_arguments_file: str) -> None:
        codeunit_file = os.path.join(repo_folder, codeunit_name, codeunit_name + ".codeunit.xml")
        dependent_codeunits = self.get_dependent_code_units(codeunit_file)
        dependent_codeunits_folder = os.path.join(repo_folder, codeunit_name, "Other", "Resources", "DependentCodeUnits")
        GeneralUtilities.ensure_directory_does_not_exist(dependent_codeunits_folder)
        if 0 < len(dependent_codeunits):
            GeneralUtilities.write_message_to_stdout(f"Start building dependent codeunits for codeunit {codeunit_name}.")
        for dependent_codeunit in dependent_codeunits:
            self.__build_codeunit(os.path.join(repo_folder, dependent_codeunit), verbosity, target_environmenttype, additional_arguments_file)
        if 0 < len(dependent_codeunits):
            GeneralUtilities.write_message_to_stdout(f"Finished building dependent codeunits for codeunit {codeunit_name}.")

    @GeneralUtilities.check_arguments
    def copy_artifacts_from_dependent_code_units(self, repo_folder: str, codeunit_name: str) -> None:
        GeneralUtilities.write_message_to_stdout(f"Get dependent artifacts for codeunit {codeunit_name}.")
        codeunit_file = os.path.join(repo_folder, codeunit_name, codeunit_name + ".codeunit.xml")
        dependent_codeunits = self.get_dependent_code_units(codeunit_file)
        dependent_codeunits_folder = os.path.join(repo_folder, codeunit_name, "Other", "Resources", "DependentCodeUnits")
        GeneralUtilities.ensure_directory_does_not_exist(dependent_codeunits_folder)
        for dependent_codeunit in dependent_codeunits:
            target_folder = os.path.join(dependent_codeunits_folder, dependent_codeunit)
            GeneralUtilities.ensure_directory_does_not_exist(target_folder)
            other_folder = os.path.join(repo_folder, dependent_codeunit, "Other")
            artifacts_folder = os.path.join(other_folder, "Artifacts")
            shutil.copytree(artifacts_folder, target_folder)

    @GeneralUtilities.check_arguments
    def add_github_release(self, productname: str, projectversion: str, build_artifacts_folder: str, github_username: str, repository_folder: str,
                           verbosity: int, commandline_arguments: list[str]):
        verbosity = TasksForCommonProjectStructure.get_verbosity_from_commandline_arguments(commandline_arguments, verbosity)
        github_repo = f"{github_username}/{productname}"
        artifacts_files = [file for file in GeneralUtilities.get_direct_files_of_folder(f"{build_artifacts_folder}\\{productname}\\{projectversion}") if file.endswith(".zip")]
        changelog_file = os.path.join(repository_folder, "Other", "Resources", "Changelog", f"v{projectversion}.md")
        self.__sc.run_program_argsasarray("gh", ["release", "create", f"v{projectversion}", "--repo",  github_repo,
                                                 "--notes-file", changelog_file, "--title", f"Release v{projectversion}"]+artifacts_files, verbosity=verbosity)

    @GeneralUtilities.check_arguments
    def standardized_tasks_update_version_in_docker_examples(self, file, codeunit_version):
        folder_of_current_file = os.path.dirname(file)
        codeunit_folder = GeneralUtilities.resolve_relative_path("..", folder_of_current_file)
        codeunit_name = os.path.basename(codeunit_folder)
        codeunit_name_lower = codeunit_name.lower()
        examples_folder = GeneralUtilities.resolve_relative_path("Other/Examples", codeunit_folder)
        for example_folder in GeneralUtilities.get_direct_folders_of_folder(examples_folder):
            docker_compose_file = os.path.join(example_folder, "docker-compose.yml")
            if os.path.isfile(docker_compose_file):
                filecontent = GeneralUtilities.read_text_from_file(docker_compose_file)
                replaced = re.sub(f'image:\\s+[\'"]{codeunit_name_lower}:\\d+\\.\\d+\\.\\d+[\'"]', f"image: '{codeunit_name_lower}:{codeunit_version}'", filecontent)
                GeneralUtilities.write_text_to_file(docker_compose_file, replaced)

    @GeneralUtilities.check_arguments
    def run_dockerfile_example(self, current_file: str, verbosity: int = 3, remove_old_container: bool = False, commandline_arguments: list[str] = []):
        verbosity = TasksForCommonProjectStructure.get_verbosity_from_commandline_arguments(commandline_arguments, verbosity)
        folder = os.path.dirname(current_file)
        example_name = os.path.basename(folder)
        GeneralUtilities.write_message_to_stdout(f'Run "{example_name}"-example')
        sc = ScriptCollectionCore()
        oci_image_artifacts_folder = GeneralUtilities.resolve_relative_path("../../Artifacts/BuildResult_OCIImage", folder)
        image_filename = os.path.basename(sc.find_file_by_extension(oci_image_artifacts_folder, "tar"))
        codeunit_name = os.path.basename(GeneralUtilities.resolve_relative_path("../../..", folder))
        codeunit_name_lower = codeunit_name.lower()
        if remove_old_container:
            GeneralUtilities.write_message_to_stdout(f"Ensure container {codeunit_name_lower} does not exist...")
            sc.run_program("docker", f"container rm -f {codeunit_name_lower}", oci_image_artifacts_folder, verbosity=verbosity)
        GeneralUtilities.write_message_to_stdout("Load docker-image...")
        sc.run_program("docker", f"load -i {image_filename}", oci_image_artifacts_folder, verbosity=verbosity)
        project_name = f"{codeunit_name}_{example_name}".lower()
        sc.program_runner = ProgramRunnerEpew()
        GeneralUtilities.write_message_to_stdout("Start docker-container...")
        sc.run_program("docker-compose", f"--project-name {project_name} up", folder, verbosity=verbosity)

    @GeneralUtilities.check_arguments
    def __create_archive_of_artifacts(self, codeunitname: str, version: str, build_artifacts_folder: str, build_environment_target_type: str, remove_build_artifacts: bool):
        filename_without_extension = f"{codeunitname}.v{version}.{build_environment_target_type}.Artifacts"
        working_dir = os.path.dirname(build_artifacts_folder)
        temp_folder = os.path.join(working_dir, filename_without_extension)
        GeneralUtilities.ensure_directory_does_not_exist(temp_folder)
        content_folder = os.path.join(temp_folder, filename_without_extension)
        GeneralUtilities.ensure_directory_exists(content_folder)
        GeneralUtilities.copy_content_of_folder(build_artifacts_folder, content_folder)
        filename = f"{filename_without_extension}.zip"
        GeneralUtilities.ensure_file_does_not_exist(filename)
        shutil.make_archive(filename_without_extension, 'zip', temp_folder)
        shutil.move(filename, working_dir)
        GeneralUtilities.ensure_directory_does_not_exist(temp_folder)
        if remove_build_artifacts:
            GeneralUtilities.ensure_directory_does_not_exist(build_artifacts_folder)

    @GeneralUtilities.check_arguments
    def _internal_sort_codenits(self, codeunits=dict[str, set[str]]) -> list[str]:
        result: list[str] = list[str]()
        ts = TopologicalSorter(codeunits)
        result = list(ts.static_order())
        return result

    @GeneralUtilities.check_arguments
    def build_codeunits(self, repository_folder: str, verbosity: int = 1, target_environmenttype: str = "QualityCheck", additional_arguments_file: str = None,
                        is_pre_merge: bool = False, export_target_directory: str = None) -> None:
        codeunits: dict[str, set[str]] = dict[str, set[str]]()
        subfolders = GeneralUtilities.get_direct_folders_of_folder(repository_folder)
        for subfolder in subfolders:
            codeunit_name: str = os.path.basename(subfolder)
            codeunit_file = os.path.join(subfolder, f"{codeunit_name}.codeunit.xml")
            if os.path.exists(codeunit_file):
                codeunits[codeunit_name] = self.get_dependent_code_units(codeunit_file)
        sorted_codeunits = self._internal_sort_codenits(codeunits)
        if len(sorted_codeunits) == 0:
            raise ValueError(f'No codeunit found in subfolders of "{repository_folder}".')
        else:
            if verbosity > 1:
                GeneralUtilities.write_message_to_stdout("Attempt to build codeunits in the following order:")
                i = 0
                for codeunit in sorted_codeunits:
                    i = i+1
                    GeneralUtilities.write_message_to_stdout(f"{i}.: {codeunit}")
            for codeunit in sorted_codeunits:
                self.__build_codeunit(os.path.join(repository_folder, codeunit), verbosity, target_environmenttype, additional_arguments_file, is_pre_merge, True)
        if export_target_directory is not None:
            project_name = os.path.basename(repository_folder)
            project_version = self.get_version_of_project(repository_folder)
            for codeunit in sorted_codeunits:
                target_folder = os.path.join(export_target_directory, project_name, project_version, codeunit, "Artifacts")
                GeneralUtilities.ensure_directory_does_not_exist(target_folder)
                GeneralUtilities.ensure_directory_exists(target_folder)
                GeneralUtilities.copy_content_of_folder(os.path.join(repository_folder, codeunit, "Other", "Artifacts"), target_folder)
                self.__create_archive_of_artifacts(project_name, project_version, target_folder, target_environmenttype, target_environmenttype != "Productive")

    @GeneralUtilities.check_arguments
    def __build_codeunit(self, codeunit_folder: str, verbosity: int = 1, target_environmenttype: str = "QualityCheck", additional_arguments_file: str = None,
                         is_pre_merge: bool = False, assume_dependent_codeunits_are_already_built: bool = False) -> None:
        now = datetime.now()
        codeunit_folder = GeneralUtilities.resolve_relative_path_from_current_working_directory(codeunit_folder)
        codeunit_name: str = os.path.basename(codeunit_folder)
        codeunit_file = os.path.join(codeunit_folder, f"{codeunit_name}.codeunit.xml")
        if (not os.path.isfile(codeunit_file)):
            raise ValueError(f'"{codeunit_folder}" is no codeunit-folder.')
        artifacts_folder = os.path.join(codeunit_folder, "Other", "Artifacts")
        GeneralUtilities.write_message_to_stdout(f"Start building codeunit {codeunit_name}.")
        GeneralUtilities.write_message_to_stdout(f"Build-environmenttype: {target_environmenttype}")

        other_folder = os.path.join(codeunit_folder, "Other")
        build_folder = os.path.join(other_folder, "Build")
        quality_folder = os.path.join(other_folder, "QualityCheck")
        reference_folder = os.path.join(other_folder, "Reference")
        additional_arguments_c: str = ""
        additional_arguments_b: str = ""
        additional_arguments_r: str = ""
        additional_arguments_l: str = ""
        additional_arguments_g: str = ""
        general_argument = f'--overwrite_verbosity={str(verbosity)} --overwrite_targetenvironmenttype={target_environmenttype}'

        c_additionalargumentsfile_argument = ""

        if is_pre_merge:
            general_argument = general_argument+" --overwrite_is_pre_merge=true"
            GeneralUtilities.write_message_to_stdout("This is a pre-merge-build")

        if assume_dependent_codeunits_are_already_built:
            c_additionalargumentsfile_argument = c_additionalargumentsfile_argument+" --overwrite_assume_dependent_codeunits_are_already_built=true"
            GeneralUtilities.write_message_to_stdout("Assume dependent codeunits are already built")

        if additional_arguments_file is not None:
            config = configparser.ConfigParser()
            config.read(additional_arguments_file)
            section_name = f"{codeunit_name}_Configuration"
            if config.has_option(section_name, "ArgumentsForCommonTasks"):
                additional_arguments_c = config.get(section_name, "ArgumentsForCommonTasks")
            if config.has_option(section_name, "ArgumentsForBuild"):
                additional_arguments_b = config.get(section_name, "ArgumentsForBuild")
            if config.has_option(section_name, "ArgumentsForRunTestcases"):
                additional_arguments_r = config.get(section_name, "ArgumentsForRunTestcases")
            if config.has_option(section_name, "ArgumentsForLinting"):
                additional_arguments_l = config.get(section_name, "ArgumentsForLinting")
            if config.has_option(section_name, "ArgumentsForGenerateReference"):
                additional_arguments_g = config.get(section_name, "ArgumentsForGenerateReference")
            c_additionalargumentsfile_argument = f'--overwrite_additionalargumentsfile="{additional_arguments_file}"'

        GeneralUtilities.write_message_to_stdout('Run "CommonTasks.py"...')
        self.__sc.run_program("python", f"CommonTasks.py {additional_arguments_c} {general_argument} {c_additionalargumentsfile_argument}", other_folder, verbosity=verbosity)
        GeneralUtilities.write_message_to_stdout('Run "Build.py"...')
        self.__sc.run_program("python", f"Build.py {additional_arguments_b} {general_argument}",  build_folder, verbosity=verbosity)
        GeneralUtilities.write_message_to_stdout('Run "RunTestcases.py"...')
        self.__sc.run_program("python", f"RunTestcases.py {additional_arguments_r} {general_argument}", quality_folder, verbosity=verbosity)
        GeneralUtilities.write_message_to_stdout('Run "Linting.py"...')
        self.__sc.run_program("python", f"Linting.py {additional_arguments_l} {general_argument}", quality_folder, verbosity=verbosity)
        GeneralUtilities.write_message_to_stdout('Run "GenerateReference.py"...')
        self.__sc.run_program("python", f"GenerateReference.py {additional_arguments_g} {general_argument}", reference_folder, verbosity=verbosity)

        artifactsinformation_file = os.path.join(artifacts_folder, f"{codeunit_name}.artifactsinformation.xml")
        version = self.get_version_of_codeunit(codeunit_file)
        GeneralUtilities.ensure_file_exists(artifactsinformation_file)
        artifacts_list = []
        for artifact_folder in GeneralUtilities.get_direct_folders_of_folder(artifacts_folder):
            artifact_name = os.path.basename(artifact_folder)
            artifacts_list.append(f"        <cps:artifact>{artifact_name}<cps:artifact>")
        artifacts = '\n'.join(artifacts_list)
        moment = GeneralUtilities.datetime_to_string(now)
        # TODO implement usage of self.reference_latest_version_of_xsd_when_generating_xml
        GeneralUtilities.write_text_to_file(artifactsinformation_file, f"""<?xml version="1.0" encoding="UTF-8" ?>
<cps:artifactsinformation xmlns:cps="https://projects.aniondev.de/PublicProjects/Common/ProjectTemplates/-/tree/main/Conventions/RepositoryStructure/CommonProjectStructure" artifactsinformationspecificationversion="1.0.0"
    xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="https://raw.githubusercontent.com/anionDev/ProjectTemplates/main/Templates/Conventions/RepositoryStructure/CommonProjectStructure/artifactsinformation.xsd">
    <cps:name>{codeunit_name}</cps:name>
    <cps:version>{version}</cps:version>
    <cps:timestamp>{moment}</cps:timestamp>
    <cps:targetenvironmenttype>{target_environmenttype}</cps:targetenvironmenttype>
    <cps:artifacts>
{artifacts}
    </cps:artifacts>
</cps:artifactsinformation>""")
        # TODO validate artifactsinformation_file against xsd
        shutil.copyfile(codeunit_file,
                        os.path.join(artifacts_folder, f"{codeunit_name}.codeunit.xml"))
        GeneralUtilities.write_message_to_stdout(f"Finished building codeunit {codeunit_name}.")
