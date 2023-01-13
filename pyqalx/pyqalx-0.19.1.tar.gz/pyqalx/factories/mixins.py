"""
Mix-in classes for the main factory class. Each one of the classes in this module
contains functionality for a specific factories related stage. Keeping methods
contained in these mix-ins keeps the main factory class cleaner
"""

import concurrent.futures
import logging
import shutil
from subprocess import Popen, PIPE, CalledProcessError
import sys
import uuid
from time import sleep

from pyqalx.factories.debug import FactoryPlanDebug

try:
    import git
except ImportError:
    # ImportError: Most likely git is not in the expected place.  Not an issue
    #   unless the user wants to use bot_sources.GitBotSource
    pass
import os
import stat
import yaml
from yaml import YAMLError

from bson_extra import bson_extra

from pyqalx.config import UserConfig, BotConfig
from pyqalx.factories.bot_sources import BotSource, QalxItemBotSource
from pyqalx.core.entities.factory import Factory as FactoryEntity
from pyqalx.core.errors import (
    QalxFactoryPackError,
    QalxFactoryBuildError,
    QalxFactoryError,
    QalxAPIResponseError,
)
from pyqalx.core.errors import QalxFactoryValidationError
from pyqalx.factories.sectors.manager import SectorManager
from pyqalx.factories.sectors.sectors import Sectors
from pyqalx.factories.sectors.providers import (
    _providers,
    LocalProvider,
    AWSProvider,
)
from pyqalx.factories.tree import QalxTree
from pyqalx.core.utils import _msg_user

default_aws_profile = AWSProvider.default_profile_name()


class FactoryValidateMixin:
    """Specific Validate functionality"""

    @staticmethod
    def load_plan(plan_yml):
        """
        Loads the plan from yaml to JSON
        :param plan_yml: The plan as a yaml string
        :return: The plan as JSON
        :raises QalxFactoryError if there was a problem parsing the yaml to JSON
        """
        try:
            return yaml.safe_load(plan_yml)
        except YAMLError as exc:
            raise QalxFactoryError(
                f"There was an error parsing the plan yaml file:\n\n{exc}"
            )

    @staticmethod
    def read_plan(plan_path):
        """
        Reads a .yaml file that contains the definition of the factory plan and
        then returns it as a yaml string

        :param plan_path:   A local path to the .yaml file that contains the
                            factory plan definition

        :return:    The plan as a yaml string

        :raises QalxFactoryValidationError:     If the .yaml file does not
                                                exist
        """
        if not os.path.exists(plan_path):
            raise QalxFactoryValidationError(
                f"The plan path: {plan_path} was not found"
            )
        with open(plan_path, "r") as plan_file:
            plan = plan_file.read()
        return plan


class FactoryPackMixin:
    """Specific Pack functionality"""

    def _create_build_path(self):
        """
        Creates the build path where the bot code will live.  By default
        this will use a random uuid as we won't have a Factory entity as the
        point of packing.

        :raises QalxFactoryPackError: if
                 the directory can not be created.
        """
        try:
            os.makedirs(self.build_path)
        except (OSError, PermissionError) as exc:
            raise QalxFactoryPackError(
                f"There was an error creating the build directory\n\n{exc}"
            )

    def _bots_for_pack(self, stage=None):
        """
        Returns the bots key from the plan.  If `stage` is provided then return
        only those bots that match that stage

        :param stage: If provided, will return the bots in `factory:bots` on
        the plan that match the given stage.  If not provided, returns all bots
        :type stage: str
        :return: A dict of `bot_name:bot_source`
        """
        bots = self._plan_bots
        if stage is not None:
            # A stage was provided, only return bots that match that specific
            # stage
            _stage = self._plan_stages[stage]
            bot_names = set()
            for sector in _stage.values():
                sector_bots = isinstance(sector, dict) and sector.get("bots")
                if sector_bots:
                    bot_names.update(sector_bots.keys())
            bots = dict(filter(lambda i: i[0] in bot_names, bots.items()))
        return bots

    def _download_bot(self, bot_name, bot):
        """
        Attempts to download the given bot from the given source.

        :param bot_name:The name of the bot that is being downloaded
        :param bot:The dict representing the source bot from the plan
        """

        try:
            BotSourceClass = BotSource.get_source(bot)
        except KeyError as exc:
            raise QalxFactoryPackError(exc)
        bot_source = BotSourceClass(
            bot_name, bot, self.build_path, log=self.session.log
        )
        bot_source.download_bot()
        self.bot_sources.append(bot_source)

    def _download_bots(self, bots):
        """
        Iterates through the given bots and attempts to download them.
        Catches any potential error that could be raised and reraises as a
        QalxFactoryPackError for consistency

        :param bots:    A dictionary of {bot_name:bot_source}
        :type  bots:    dict
        :raises QalxFactoryPackError:
        """
        results = []
        exception = None
        with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
            for bot_name, bot in bots.items():
                results.append(
                    executor.submit(self._download_bot, bot_name, bot)
                )
            for result in concurrent.futures.as_completed(results):
                try:
                    # Check if there was an error downloading the bot
                    result.result()
                except (
                    git.GitCommandError,
                    CalledProcessError,
                    NotADirectoryError,
                    PermissionError,
                    FileNotFoundError,
                    QalxFactoryPackError,
                    QalxFactoryValidationError,
                ) as exc:
                    # Provides a common way of handling all the potential errors
                    # that could occur when packing bots

                    # git.GitCommandError: There was an error clone the git repo
                    # subprocess.CalledProcessError: There was an error pip
                    #                                downloading the package
                    # NotADirectoryError: The specified file wasn't a directory
                    # FileNotFoundError: The local path could not be found
                    # PermissionError: No permission to read from directory
                    # QalxFactoryValidationError: Error validating bot path

                    # Grab this exception and raise later.  Need to wait for
                    # all processing to finish before exiting otherwise it won't
                    # be possible to tidy up properly as a thread could be
                    # writing to the directory as the deletion occurs
                    exception = exc

        if exception is not None:
            # Ensure that the packing tidies up anything that was successful
            # before this failure
            self._delete_build_path()
            raise QalxFactoryPackError(exception)


class FactoryBuildMixin:
    """
    Specific build functionality
    """

    @staticmethod
    def _metadata(entity, plan_bot_name=None):
        """
        The base metadata that should be stored on any entities that are linked
        to this factory
        """
        metadata = {
            "_class": "pyqalx.factory",
            # Namedspaced metadata to avoid potential name clashing
            # with any custom metadata provided by the user.
            BaseFactory.PYQALX_METADATA_NAMESPACE_KEY: {
                BaseFactory.PYQALX_METADATA_STAGE_KEY: entity.stage,
                BaseFactory.PYQALX_METADATA_FACTORY_GUID_KEY: entity.guid,
            },
        }
        if plan_bot_name is not None:
            # This enables identification between Bot entities
            # and Item entities that contain the Bot code.
            metadata[BaseFactory.PYQALX_METADATA_NAMESPACE_KEY][
                BaseFactory.PYQALX_METADATA_PLAN_BOT_NAME_KEY
            ] = plan_bot_name
        return metadata

    def _add_entity(self, plan):
        """
        Helper for adding a factory entity to the API.
        :param plan: The path to the plan file
        :type plan:str
        :return: ~pyqalx.core.entities.factory.Factory
        """
        factory_meta = self._plan_meta
        factory_meta[self.PYQALX_METADATA_NAMESPACE_KEY] = {
            self.PYQALX_METADATA_BUILD_PATH_KEY: os.path.basename(
                self.build_path
            )
        }
        self.entity = self.session.factory.add(
            name=self._plan_name,
            source=plan,
            stage=self.stage,
            meta=factory_meta,
        )
        return self.entity

    def _create_bot_items(self):
        """
        Creates a qalx item with the code and metadata about the code of each
        bot on a factory stage. For each bot and bot source, a qalx item is
        created with the following specification:

            source: An input file is provided and it is the zipped
                        directory of the bot source code
            meta:       The metadata, with the following key/value pairs:
                "_class":           "pyqalx.factory"
                "stage:             The stage that the bots belong to
                "deployment_id":    The factory deployment id
                "md5_hash":         The md5 checksum of the contents of the bot
                                    source code directory
        """
        item_dict_list = []
        hashes = {}
        with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
            for bot_source in self.bot_sources:
                hashes[executor.submit(bot_source.get_hash)] = bot_source
            for future in concurrent.futures.as_completed(hashes):
                bot_source = hashes[future]
                plan_bot_name = bot_source.bot_name
                meta = self._metadata(
                    entity=self.entity, plan_bot_name=plan_bot_name
                )
                meta["md5_hash"] = bot_source.md5_hash
                item = {"meta": meta}
                zip_path = bot_source.zip_build_path()
                if zip_path:
                    # pypi bots won't have a file
                    item["source"] = zip_path
                item_dict_list.append(item)
        self.bot_items = self.session.item.add_many(item_dict_list).items_

    @staticmethod
    def _sanitise_cli_key(k):
        """
        For the given arguments given to `bot-start` we need to ensure that
        the keys are sanitised in case the user provides a key with either `--`
        or `-` in the plan (or they didn't provide either)
        :param k: The key to sanitise
        :type k: str
        :return: The sanitised key - with the correct number of hyphens
        prefixing it depending on whether they gave the short or longform
        argument
        """
        if k.startswith("--"):
            k = k[2:]
        elif k.startswith("-"):
            k = k[1:]
        if len(k) > 1:
            return f"--{k}"
        return f"-{k}"

    @staticmethod
    def _environment_variable_key(parameter_name):
        """
        From the given parameter name, will return the name that the environment
        variable should be
        :param name:The given parameter name in the format:
        "<factory_guid>-<ec2instancename>_<CONFIG_KEY_PREFIX>_<PARAMETER_NAME>"
        :return:"<CONFIG_KEY_PREFIX>_<PARAMETER_NAME>
        """
        return parameter_name.split("_", 1)[-1]

    def bootstrap_environment(self, ProviderClass, region_name, instance_name):
        """
        Bootstraps the environment by getting all the parameters stored on the
        cloud provider and saving them to the environment for the config to find
        :param ProviderClass:The class of the provider that is bootstrapping
        the bots
        :type ProviderClass:~factories.factory.sectors.providers.provider.BaseProvider
        :param region_name:The remote region that is used for bootstrapping the instance
        :type region_name:str
        :param instance_name:The name of the instance used when creating the stack
        :type instance_name:str
        """
        provider = ProviderClass(
            factory=self,
            # We won't have the stack or profile on remote sectors at this
            # point as we won't have been able to query the API yet to get the data.
            stack={},
            profile_name=None,
            region_name=region_name,
        )
        # There will be no config at this point so just use the
        # raw factory_guid
        provider.set_environment_variables(instance_name=instance_name)
        # Reload the current session so that it has the updated values
        # from the environment variables.  skip_ini is True because config
        # will be loading from the environment variables.  Ensure config_class
        # remains the same
        self.session = self.session.__class__(
            config_class=self.session.config.__class__, skip_ini=True
        )

    def bootstrap_bots(
        self,
        factory_guid,
        sector_name,
        profile_name,
        region_name,
        instance_name,
        ProviderClass,
    ):
        """
        Iterates through all the bots on the provided sector_name and downloads
        the code from the Items on qalx.  Once this is successful will then
        start the bots in the same way as bots on local sectors are started.
        :param factory_guid:The factory_guid that should be bootstrapped
        :param sector_name: The sector name that contains the bots that are
        being bootstrapped
        :type sector_name: str
        :param profile_name: The profile_name of the sector being bootstrapped
        :param region_name: The region_name of the sector being bootstrapped
        :param instance_name: The name of the instance being bootstrapped.
        The name must match the name used for parameters that are created
        during stack creation
        :param ProviderClass:The class of the provider that is doing the
        bootstrapping
        :type ProviderClass: A subclass of ~providers.provider.BaseProvider
        """
        self.bootstrap_environment(
            ProviderClass=ProviderClass,
            region_name=region_name,
            instance_name=instance_name,
        )
        # Get the factory and load the sectors
        self.entity = factory_guid
        sectors = Sectors(
            self, validate_default_region=False, validate_permissions=False
        )

        sector = sectors[ProviderClass._type][profile_name][region_name][
            sector_name
        ]
        # All the bot names across the approriate sectors.  A single sector
        # could have multiple bots
        bot_names = list(sector["bots"].keys())

        # Ensure that the build_path gets created so that the bot code can be
        # downloaded.  Ensure the build path is deleted first.  It could exist
        # if the instance has been rebooted - in which case we act as if it's
        # the first boot to handle updates more easily.
        self._delete_build_path()
        self._create_build_path()

        namespace_key = self.PYQALX_METADATA_NAMESPACE_KEY
        factory_guid_key = self.PYQALX_METADATA_FACTORY_GUID_KEY
        plan_bot_name_key = self.PYQALX_METADATA_PLAN_BOT_NAME_KEY
        # Get just the code items that relate to the bots we are bootstrapping
        query = f"metadata.data.{namespace_key}"
        items = self.session.item.find(
            query={
                f"{query}.{factory_guid_key}": self.entity.guid,
                f"{query}.{plan_bot_name_key}": {"$in": bot_names},
            }
        )

        # Iterate through all the bot code items that we are starting the bots
        # for, download the code and then start the bot (async)
        results = []
        start_context = {}
        max_workers = items.query.count
        with concurrent.futures.ThreadPoolExecutor(
            max_workers=max_workers
        ) as executor:
            for bot_code_item in items.data:
                bot_name = bot_code_item.meta[namespace_key][plan_bot_name_key]
                bot = self._plan_bots[bot_name]
                bot_source = QalxItemBotSource(
                    bot_name=bot_name,
                    bot=bot,
                    build_path_dir=self.build_path,
                    bot_code_item=bot_code_item,
                    log=self.session.log,
                )
                results.append(executor.submit(bot_source.download_bot))

                # Context required when the download is completed so that the
                # bot can be started
                bot_arguments = sector["bots"][bot_name]

                start_context[bot_name] = {
                    "build_path": bot_source.build_path,
                    "plan_bot_name": bot_name,
                    "bot_path": bot["bot_path"],
                    "bot_arguments": bot_arguments,
                    "sector": sector,
                    "skip_ini": True,
                }

            for future in concurrent.futures.as_completed(results):
                # As the downloads complete, start the bots up.
                output, error = self.start_bot(**start_context[future.result()])
                if output.returncode is not None:
                    # There was an error starting up this bot. Raise an
                    # exception as this needs to be handled by the bootstrap
                    # script itself which will take appropriate action.
                    raise QalxFactoryBuildError(str(error))

    def start_bot(
        self,
        plan_bot_name,
        build_path,
        bot_path,
        bot_arguments,
        sector,
        skip_ini=False,
    ):
        """
        Starts a single bot in an orphaned subprocess. Enables factories to start
        multiple bots without blocking.
        :param plan_bot_name:The name of the bot from the plan
        :type plan_bot_name:str
        :param build_path:The path where the bot source resides
        :type build_path: str
        :param bot_path:The path to the bot to be used in the start call
        :type bot_path:str
        :param bot_arguments:Any additional parameters to be passed to start
        :type bot_arguments: dict
        :param sector:The specific sector that contains this bot
        :type sector: dict
        :param skip_ini:Should the initialisation of the qalx session be skipped?
        :type skip_ini:bool
        :return:The output of the subprocess call and any errors that occurred.
        """
        arguments = []

        for k, v in bot_arguments.items():
            arguments += [FactoryBuildMixin._sanitise_cli_key(k), str(v)]

        if skip_ini:
            # Remote bots won't have access to a config file.
            arguments.append("--skip-ini")

        # All bots should be started but in a "stopped" state.
        # This will enable all bots to be created before any start
        # processing data
        arguments.append("--stop")
        metadata = FactoryBuildMixin._metadata(
            entity=self.entity, plan_bot_name=plan_bot_name
        )
        stage_workflow = self._plan_stage.get("workflow")
        if stage_workflow:
            plan_workflow = self._plan_workflows[stage_workflow]
            successors = plan_workflow.get_successors(plan_bot_name)

            # If the bot isn't part of the workflow, don't add the extra args
            if successors:
                for successor in successors:
                    arguments += ["--workflow", successor]

        for key, value in metadata.items():
            # Builds the meta data to be saved on the bot
            if not isinstance(value, str):
                # This value isn't a string.  Dump to JSON so it can be saved it
                # in the correct structure
                value = bson_extra.dumps(value)
            arguments += ["--meta", f"{key}={value}"]

        # subprocess will be called using the same environment as the main
        # process.  However, this won't know about the path for the bot as
        # this gets updated at runtime .  Add the package on the build path
        # (just for the context of this subprocess
        # call).  We then need to pass the full environment through to
        # subprocess along with the modified path so that the bot can be
        # imported.
        modified_env = os.environ.copy()
        modified_path = sys.path + [build_path]
        python_path = os.pathsep.join(modified_path)
        modified_env["PYTHONPATH"] = python_path

        qalx = shutil.which("qalx")

        output = Popen(
            [
                qalx,
                "--user-profile",
                sector[Sectors.USER_PROFILE_KEY],
                "--bot-profile",
                sector[Sectors.BOT_PROFILE_KEY],
                "bot-start",
                *arguments,
                bot_path,
            ],
            # Redirect stderr and stdout to PIPE so we can capture
            # errors to give to the user in the main thread
            stdout=PIPE,
            stderr=PIPE,
            env=modified_env,
        )

        # Arbitrary timeout to give the bot a chance to start.
        # TODO: Handle getting the bot and checking the status of the
        #  workers to ensure it's been created successfully.  Will allow quicker
        # startups
        sleep(10)
        # .poll() will populate the returncode for us - but nothing else
        output.poll()
        error = None
        if output.returncode is not None:
            # Some sort of error occurred when starting this bot
            stdout, stderr = output.communicate()
            # There might be an error on `stdout` if there was an exception
            # raised i.e. in the config if the log file path
            # couldn't be created.  Therefore, join stdout and stderr together
            # (giving more prominence to stderr) just in case there are issues
            # in two places.
            error = "\n".join([stderr.decode("utf-8"), stdout.decode("utf-8")])
        return output, error

    def _create_stacks(self):
        """
        Creates the stacks for each bot. A stack is all the resources for the
        bots on a sector with an intersection of profile_name/region_name.  All
        local bots will be on their own stack, whereas remote bots will be
        separated out into separate sectors on stacks which share a
        profile_name/region_name.
        When this completes successfully all the bots will have been started in
        a stopped state.
        If there are any issues with creating a stack (i.e. stack creation fails,
        bot fails to start etc) then all stacks get deleted and the user
        is given an error.
        """
        providers = {}
        stack_mapping = {}
        with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
            # Synchronously start the processes.  Local bots will have a sleep
            # in the main thread but that shouldn't cause remote stacks to
            # not be started as soon as possible.
            for _provider in self.stacks:
                if _provider is not None:
                    # Provider will be None if a provider is not configured
                    # properly
                    providers[
                        executor.submit(_provider.create_stack)
                    ] = _provider
            for future in concurrent.futures.as_completed(providers):
                provider = providers[future]
                for sector_name in provider.stack.keys():
                    # Ensure the sectors are saved against the stack ids
                    # - only remote sectors are saved.
                    if not isinstance(provider, LocalProvider):
                        stack_mapping[sector_name] = provider.stack_id

        # Add the stack mappings to the entity for later saving.
        self.entity["stacks"] = stack_mapping
        all_completed = False
        if providers:
            # Only run the manager if there are providers - if there aren't
            # any then there was a config error with one/all the providers
            manager = SectorManager(
                providers=list(providers.values()), plan_debug=self._plan_debug
            )
            manager._monitor_stack_creation()
            all_completed = manager._all_completed()

        if all_completed or self._plan_debug._demolish_on_failure is False:
            # Add the stack mappings to the entity if the stacks
            # created successfully or if we the debug key is set to not demolish
            # on failure.
            self.entity["stacks"] = stack_mapping
            self.session.factory.save(self.entity)
        return all_completed

    def _add_factory_bots(self):
        """
        Updates the factory entity with the Bot entities and the
        Item entities that the Bot code is stored on.  The `plan_bot_name` is
        stored in metadata on the Item and the Bot which can be used to figure
        out how they are related.
        """
        namespace_key = self.PYQALX_METADATA_NAMESPACE_KEY
        plan_bot_name_key = self.PYQALX_METADATA_PLAN_BOT_NAME_KEY
        item_bot_name_to_guid = {
            item.meta[namespace_key][plan_bot_name_key]: item.guid
            for item in self.bot_items
        }

        expected_build_bots = []
        for bot_guid, plan_bot_name in self.bots.keys():
            # There could be more bot entities than item entities if the same
            # bot is used on multiple sectors.
            expected_build_bots.append(
                {"code": item_bot_name_to_guid[plan_bot_name], "bot": bot_guid}
            )
        self.entity["bots"] = expected_build_bots
        self.session.factory.save(self.entity)

    def _resume_bots(self):
        """
        Once all the bots are successfully created then they should be resumed.
        """
        for bot in self.bots.values():
            self.session.bot.resume(bot)


class FactoryDemolishMixin:
    """
    Specific Demolish functionality

    Class Attributes
        MAX_BOT_TERMINATE_PROCESSES:    Maximum number of processes to allow for
                                        terminating bots
    """

    MAX_BOT_TERMINATE_PROCESSES = 4

    def get_workflow(self):
        """
        Get the workflow according to which the factory has been deployed. If no
        workflow has been specified for the deployed stage of the factory, then
        a "flat" workflow with all the bots on the factory entity at the same
        level is returned

        :return: The workflow of the deployed stage which is a QalxTree instance
        """
        workflow_key = self._plan_stage.get("workflow")
        bot_names = list(
            set([bot_plan_name for _, bot_plan_name in self.bots.keys()])
        )
        if workflow_key:
            workflow = self._plan_workflows[workflow_key]
            # We need to add leaf nodes to the tree for all the bots that are on
            # the stage, but not on the workflow definition from the plan. These
            # bots are at the top level of the tree
            for bot_name in bot_names:
                if bot_name not in workflow.nodes:
                    workflow.create_node(
                        bot_name, bot_name, parent=workflow.root
                    )
            return workflow
        return QalxTree({"flat_workflow": bot_names})

    def wait_on_bot_termination(self, bot):
        """
        For a provided bot entity, iterates through all the workers and returns
        only after it has been asserted that all workers have been warm
        terminated.

        :param bot:     The bot to wait on until all workers are warm terminated
        """

        def _terminate_warm(_bot):
            # Helper for returning the `terminate_warm` signal of all works
            # on a given bot
            return [
                self.session.worker.signal_class(_worker).terminate_warm
                for _worker in _bot.workers
            ]

        terminated_signals = _terminate_warm(bot)

        while not all(terminated_signals):
            # sleep, to prevent hitting the API too many times while waiting
            # for termination.
            sleep(5)
            bot = self.session.bot.reload(bot)
            terminated_signals = _terminate_warm(bot)

    def safe_terminate_bot(self, plan_bot_name):
        """
        Safely terminate one or more bots with the provided plan name. Calls
        bot.terminate with warm=True on the specified bots and then for each of
        the bots calls wait_on_bot_termination.  There may be multiple bots
        with the same name - i.e. same bot on different sectors.  These can
        be safely terminated in parallel as this method is only called with
        the correct bot names for the correct point in the workflow
        :param  plan_bot_name:   The name of the bot to terminate on the plan
        :type   plan_bot_name    str
        :return bot_name
        """
        self._msg_user(msg=f"[{plan_bot_name}] terminating")
        with concurrent.futures.ThreadPoolExecutor(
            max_workers=self.MAX_BOT_TERMINATE_PROCESSES
        ) as executor:
            for (_, _plan_bot_name), bot in self.bots.items():
                if _plan_bot_name == plan_bot_name:
                    # Send termination signal to all affected bots.
                    # and wait for termination to complete.
                    executor.submit(
                        self.session.bot.terminate, entity=bot, warm=True
                    )
                    executor.submit(self.wait_on_bot_termination, bot)
        self._msg_user(msg=f"[{plan_bot_name}] terminated successfully")
        return plan_bot_name

    def concurrent_terminate(self, workflow, bot_names):
        """
        Terminate a list of bots concurrently with concurrent.futures

        :param  workflow:   The workflow that has to be respected in termination
        :type   workflow:   QalxTree instance
        :param  bot_names:  The bot names to terminate
        :type   bot_names:  list
        """
        results = []
        with concurrent.futures.ThreadPoolExecutor(
            max_workers=self.MAX_BOT_TERMINATE_PROCESSES
        ) as executor:
            for bot_name in bot_names:
                results.append(
                    executor.submit(self.safe_terminate_bot, bot_name)
                )
            for finished in concurrent.futures.as_completed(results):
                bot_name = finished.result()
                try:
                    self.concurrent_terminate(
                        workflow, workflow.get_successors(bot_name)
                    )
                except QalxAPIResponseError as exc:
                    # QalxAPIResponseError:  Issue when terminating bot.
                    #                        Unlikely to happen if the user gets
                    #                        this far but they should be made
                    #                        aware so they can take manual steps
                    self._msg_user(
                        msg=f"Exception occurred when "
                        f"terminating {bot_name}.  "
                        f"You may need to terminate this "
                        f"manually: {exc} ",
                        level=logging.ERROR,
                    )

    def breadth_first_terminate(self):
        """
        Breadth-first terminate of bots for a provided tree structure of a
        workflow. Traverses the nodes of the workflow in breadth-first order and
        calls "concurrent_terminate" on the successors of each node.

        Once all the bots are terminated the stacks can be deleted.  For remote
        stacks the bot processes will exit when the stack is deleted.  For local
        stacks, the bots will just exit normally as if `qalx bot-terminate` had
        been called on them

        """
        workflow = self.get_workflow()
        successors = workflow.get_successors(workflow.root)
        self.concurrent_terminate(workflow, successors)


class BaseFactory(
    FactoryValidateMixin,
    FactoryPackMixin,
    FactoryBuildMixin,
    FactoryDemolishMixin,
):
    """
    Base factory class. Contains attributes and methods that are not tied to a
    specific stage of a factory

    Class attributes
        PYQALX_METADATA_NAMESPACE_KEY:          Metadata key for pyqalx namespace
        PYQALX_METADATA_STAGE_KEY:              Metadata key for stage
        PYQALX_METADATA_FACTORY_GUID_KEY:       Metadata key for factory guid
        PYQALX_METADATA_PLAN_BOT_NAME_KEY:      Metadata key for plan bot name

    Instance attributes
        session:        A QalxSession instance
        user_profile:   The qalx profile to use as a user profile.
        bot_profile:    The qalx profile to use for starting bots. Default value
                        is according to the default bot configuration
        aws_profile:    The AWS profile to use for remote sectors. Default value
                        is according to boto3 defaults
        __entity: The Factory entity from the API.
        __plan:           A dictionary with the details of the plan of the factory
        __stage: The stage that the build/pack is using.  Uses the stage on the

        build_path:         The root path that the bot code gets downloaded to
                            and built from
        bot_sources:    A list of BotSource instances for each of the bots
                            that are being build
        _bots: A mapping of the bot names on the plan
              to the ~pyqalx.core.entities.bot.Bot instances
    """

    PYQALX_METADATA_NAMESPACE_KEY = "pyqalx"
    PYQALX_METADATA_STAGE_KEY = "stage"
    PYQALX_METADATA_FACTORY_GUID_KEY = "factory_guid"
    PYQALX_METADATA_PLAN_BOT_NAME_KEY = "plan_bot_name"
    PYQALX_METADATA_BUILD_PATH_KEY = "build_path"

    def __init__(
        self,
        session,
        user_profile=UserConfig.default,
        bot_profile=BotConfig.default,
        aws_profile=default_aws_profile,
    ):
        """
        :param session: An instance of :class:`~pyqalx.core.session.QalxSession`
        :type session: ~pyqalx.core.session.QalxSession
        :param user_profile: The user profile to use
        :type user_profile: str
        :param bot_profile: The bot profile to user
        :type bot_profile: str
        :param aws_profile: The AWS profile to use
        :type aws_profile: str
        """
        self.session = session
        self.user_profile = user_profile
        self.bot_profile = bot_profile
        self.aws_profile = aws_profile
        self.__plan = None
        self.__entity = None
        self.__stage = None
        self.__build_path = None

        self.bot_sources = []
        self.bot_items = []
        self._bots = None

    def _msg_user(self, *args, **kwargs):
        _msg_user(log=self.session.log, *args, **kwargs)

    @property
    def build_path(self):
        """
        If there is an entity on the factory then always use the build
        path defined on the entity otherwise use a random uuid.  Caches the
        build directory on the instance to avoid the uuid changing if there
        is no entity

        :return:  The full build_path
        """
        if self.__build_path is None:
            if self.entity is not None:
                build_basename = self.entity.meta[
                    self.PYQALX_METADATA_NAMESPACE_KEY
                ][self.PYQALX_METADATA_BUILD_PATH_KEY]
            else:
                build_basename = f"builds_{uuid.uuid4()}"
            self.__build_path = os.path.join(
                self.session.config["FACTORY_PACK_DIR"], build_basename
            )
        return self.__build_path

    @property
    def entity(self):
        return self.__entity

    @entity.setter
    def entity(self, factory):
        """
        Setter for entity.  Given an instance of
        ~pyqalx.core.entities.factory.Factory will set the entity on the Factory.
        If given a UUID string will get the factory from the API
        :param factory: An instance of ~pyqalx.core.entities.factory.Factory
        or a uuid as a string
        :raises ValueError: if incorrect instance
        """

        if not isinstance(factory, FactoryEntity):
            if self.__entity is not None:
                # Caches the entity to avoid repeated lookups
                return
            try:
                uuid.UUID(str(factory))
            except ValueError:
                raise QalxFactoryError(
                    f"factory not a valid {FactoryEntity} "
                    f"or {uuid.UUID} instance."
                )

            factory = self.session.factory.get(guid=factory)
        self.__entity = factory

    @property
    def plan(self):
        """
        If there is an entity then use the plan on the entity, otherwise use
        the plan that is already set
        :return: The plan as a JSON string
        """
        if self.entity is not None:
            self.plan = self.entity._file_bytes or self.entity.read_file()
        return self.__plan

    @plan.setter
    def plan(self, plan_yaml):
        """
        Loads the plan from yaml and sets the __plan attribute as JSON
        :param plan_yaml: The plan as a yaml string
        """
        self.__plan = FactoryValidateMixin.load_plan(plan_yaml)

    @property
    def stage(self):
        """
        If there is an entity then use the stage on the entity, otherwise use
        the stage that is already set
        :return: The stage for this factory
        """
        if self.entity is not None:
            self.stage = self.entity.stage
        return self.__stage

    @stage.setter
    def stage(self, value):
        self.__stage = value

    @property
    def _plan_factory(self):
        if self.plan is None:
            raise QalxFactoryError("`plan` must be set on the instance")
        return self.plan["factory"]

    @property
    def _plan_debug(self):
        return FactoryPlanDebug(self._plan_factory.get("debug", {}))

    @property
    def _plan_name(self):
        return self._plan_factory["name"]

    @property
    def _plan_bots(self):
        """
        Helper for getting the bots from the plan
        :return: The bots from the plan
        """
        return self._plan_factory["bots"]

    @property
    def _plan_workflows(self):
        """
        Ensures that the workflows for the plan are always returned as a dict
        of QalxTree instances.  This enables easier iteration and searching of
        the workflow.  Handles there being potentiall multiple root nodes
        by creating a list or dict of the root nodes for each workflow.
        :return: A dict of {workflow_name:QalxTree instances}
        """
        tree_workflows = {}
        for workflow_name, structure in self._plan_factory["workflows"].items():
            tree_workflows[workflow_name] = QalxTree({workflow_name: structure})
        return tree_workflows

    @property
    def _plan_stages(self):
        """
        Helper for getting the stages from the plan
        :return: The stages from the plan
        """
        return self._plan_factory["stages"]

    @property
    def _plan_meta(self):
        """
        Helper for getting the meta from the plan
        :return: The meta from the plan
        """
        return self._plan_factory.get("meta", {})

    @property
    def _plan_tags(self):
        """
        Helper for getting the tags from the plan
        :return: The tags from the plan
        """
        return self._plan_factory.get("tags", {})

    @property
    def _plan_stage(self):
        return self._plan_stages[self.entity.stage]

    @property
    def stacks(self):
        """
        Iterator that returns a stack as a Provider instance.  A stack is a
        unique intersection of a provider type->profile_name->region_name.
        A stack could have multiple sectors on it.  The stack can be accessed
        from the provider instance
        :return: An instance of ~BaseProvider for a specific stack.
        """
        try:
            sectors = Sectors(factory=self)
            for _provider, stacks in sectors.items():
                for profile_name, regions in stacks.items():
                    for region_name, stack in regions.items():
                        Provider = _providers[_provider]
                        provider = Provider(
                            factory=self,
                            profile_name=profile_name,
                            region_name=region_name,
                            stack=stack,
                        )
                        yield provider
        except QalxFactoryError:
            # QalxFactoryError: There is no default region configured
            #                   for a provider
            yield None

    @property
    def bots(self):
        """
        :return: A map of {(<bot_guid>, <plan_bot_name>): <bot_entity>}
                for the bots on the factory entity
        """
        if self._bots is None:
            self._bots = {}
            namespace_key = self.PYQALX_METADATA_NAMESPACE_KEY
            plan_bot_name_key = self.PYQALX_METADATA_PLAN_BOT_NAME_KEY
            factory_guid_key = self.PYQALX_METADATA_FACTORY_GUID_KEY
            query = {
                f"metadata.data.{namespace_key}.{factory_guid_key}": self.entity.guid
            }
            bots = self.session.bot.find(query=query)

            for bot_entity in bots.data:
                plan_bot_name = bot_entity.meta[namespace_key][
                    plan_bot_name_key
                ]
                # A single plan_bot_name could spawn multiple bots in the event
                # that the same plan_bot_name is in different sectors.
                self._bots[(bot_entity.guid, plan_bot_name)] = bot_entity
        return self._bots

    def _delete_build_path(self):
        """
        Deletes the entire build path from the filesystem if it exists. If the
        directory is not found, a message is printed out
        """
        self._msg_user(
            msg=f"Deleting data from build path: `{self.build_path}`"
        )

        def remove_readonly(func, path, _):
            """Clear the readonly bit and reattempt the removal"""
            os.chmod(path, stat.S_IWRITE)
            func(path)

        if os.path.exists(self.build_path):
            shutil.rmtree(self.build_path, onerror=remove_readonly)
        else:
            self._msg_user(
                msg=f"`{self.build_path}` not found on this machine.  "
                f"Unable to delete"
            )

    def _delete_items(self):
        """
        Find all the items for the factory entity based on their
        metadata. Iterates through them deletes them from the API. In the
         case of an error from the API during the deleting process, the error
         is logged and printed out.
        """
        namespace_key = self.PYQALX_METADATA_NAMESPACE_KEY
        factory_guid_key = self.PYQALX_METADATA_FACTORY_GUID_KEY
        query = {
            f"metadata.data.{namespace_key}.{factory_guid_key}": self.entity.guid
        }
        items = self.session.item.find(query=query)
        for item in items.data:
            try:
                self.session.item.delete(item)
            except QalxAPIResponseError as exc:
                err_msg = (
                    f"There was an error deleting a qalx item containing "
                    f"factory bot code.  "
                    f"You may have to delete this manually.: {exc}"
                )
                self._msg_user(msg=err_msg, level=logging.ERROR)

    def _delete_factory_build(self):
        """
        Deletes the factory build entity from the API. In the case of an error,
        the error message is printed and logged
        """
        try:
            self.session.factory.delete(self.entity)
        except QalxAPIResponseError as exc:
            err_msg = (
                f"There was an error deleting the factory build entity.  "
                f"You may have to delete this manually.: {exc}"
            )
            self._msg_user(msg=err_msg, level=logging.ERROR)

    def _delete_stacks(self):
        """
        Iterates through all the stacks and deletes the stack from the
        remote instance.
        """
        deleted_stacks = []
        if self.entity.stacks:
            # May not be stacks if there was an error during stack creation
            for provider in self.stacks:
                if not isinstance(provider, LocalProvider):
                    # LocalProviders won't have a stack to delete.
                    for sector_name in provider.stack.keys():
                        stack_id = self.entity.stacks[sector_name]
                        if stack_id not in deleted_stacks:
                            # Multiple sectors could share the same stack.
                            # Ensure that we only call delete once per stack
                            provider.delete_stack(stack_id=stack_id)
                            deleted_stacks.append(stack_id)

    def _delete_resources(self, delete_stacks=True):
        """
        Helper method for tidying up a factory.  Could be called as part of
        demolishing, or due to a failed build
        :param delete_stacks:Should the stacks be deleted
        :type delete_stacks:bool
        """
        if delete_stacks:
            # Should the stacks be deleted?  If the stack creation failed then
            # the stacks will have deleted themselves, so deletion shouldn't
            # be attempted.  If an error occurs after stack creation then
            # the stacks should be deleted
            self._delete_stacks()
        self._delete_items()
        self._delete_factory_build()
        self._delete_build_path()
