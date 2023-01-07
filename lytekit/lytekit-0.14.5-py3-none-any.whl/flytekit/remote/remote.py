"""
This module provides the ``FlyteRemote`` object, which is the end-user's main starting point for interacting
with a Flyte backend in an interactive and programmatic way. This of this experience as kind of like the web UI
but in Python object form.
"""
from __future__ import annotations

import base64
import functools
import hashlib
import os
import time
import typing
import uuid
from collections import OrderedDict
from dataclasses import asdict, dataclass
from datetime import datetime, timedelta

from flyteidl.core import literals_pb2 as literals_pb2

from flytekit import Literal
from flytekit.clients.friendly import SynchronousFlyteClient
from flytekit.clients.helpers import iterate_node_executions, iterate_task_executions
from flytekit.configuration import Config, FastSerializationSettings, ImageConfig, SerializationSettings
from flytekit.core import constants, tracker, utils
from flytekit.core.base_task import PythonTask
from flytekit.core.context_manager import FlyteContext, FlyteContextManager
from flytekit.core.data_persistence import FileAccessProvider
from flytekit.core.launch_plan import LaunchPlan
from flytekit.core.python_auto_container import PythonAutoContainerTask
from flytekit.core.reference_entity import ReferenceSpec
from flytekit.core.type_engine import LiteralsResolver, TypeEngine
from flytekit.core.workflow import WorkflowBase
from flytekit.exceptions import user as user_exceptions
from flytekit.exceptions.user import FlyteEntityAlreadyExistsException, FlyteEntityNotExistException
from flytekit.loggers import remote_logger
from flytekit.models import common as common_models
from flytekit.models import filters as filter_models
from flytekit.models import launch_plan as launch_plan_models
from flytekit.models import literals as literal_models
from flytekit.models import task as task_models
from flytekit.models.admin import common as admin_common_models
from flytekit.models.admin import workflow as admin_workflow_models
from flytekit.models.admin.common import Sort
from flytekit.models.core import workflow as workflow_model
from flytekit.models.core.identifier import Identifier, ResourceType, WorkflowExecutionIdentifier
from flytekit.models.core.workflow import NodeMetadata
from flytekit.models.execution import (
    ExecutionMetadata,
    ExecutionSpec,
    NodeExecutionGetDataResponse,
    NotificationList,
    WorkflowExecutionGetDataResponse,
)
from flytekit.remote.executions import FlyteNodeExecution, FlyteTaskExecution, FlyteWorkflowExecution
from flytekit.remote.interface import TypedInterface
from flytekit.remote.launch_plan import FlyteLaunchPlan
from flytekit.remote.nodes import FlyteNode
from flytekit.remote.remote_callable import RemoteEntity
from flytekit.remote.task import FlyteTask
from flytekit.remote.workflow import FlyteWorkflow
from flytekit.tools.script_mode import fast_register_single_script
from flytekit.tools.translator import FlyteLocalEntity, Options, get_serializable, get_serializable_launch_plan

ExecutionDataResponse = typing.Union[WorkflowExecutionGetDataResponse, NodeExecutionGetDataResponse]

MOST_RECENT_FIRST = admin_common_models.Sort("created_at", admin_common_models.Sort.Direction.DESCENDING)


@dataclass
class ResolvedIdentifiers:
    project: str
    domain: str
    name: str
    version: str


def _get_latest_version(list_entities_method: typing.Callable, project: str, domain: str, name: str):
    named_entity = common_models.NamedEntityIdentifier(project, domain, name)
    entity_list, _ = list_entities_method(
        named_entity,
        limit=1,
        sort_by=Sort("created_at", Sort.Direction.DESCENDING),
    )
    admin_entity = None if not entity_list else entity_list[0]
    if not admin_entity:
        raise user_exceptions.FlyteEntityNotExistException("Named entity {} not found".format(named_entity))
    return admin_entity.id.version


def _get_entity_identifier(
    list_entities_method: typing.Callable,
    resource_type: int,  # from flytekit.models.core.identifier.ResourceType
    project: str,
    domain: str,
    name: str,
    version: typing.Optional[str] = None,
):
    return Identifier(
        resource_type,
        project,
        domain,
        name,
        version if version is not None else _get_latest_version(list_entities_method, project, domain, name),
    )


class FlyteRemote(object):
    """Main entrypoint for programmatically accessing a Flyte remote backend.

    The term 'remote' is synonymous with 'backend' or 'deployment' and refers to a hosted instance of the
    Flyte platform, which comes with a Flyte Admin server on some known URI.
    """

    def __init__(
        self,
        config: Config,
        default_project: typing.Optional[str] = None,
        default_domain: typing.Optional[str] = None,
        data_upload_location: str = "s3://my-s3-bucket/data",
        **kwargs,
    ):
        """Initialize a FlyteRemote object.

        :type kwargs: All arguments that can be passed to create the SynchronousFlyteClient. These are usually grpc
            parameters, if you want to customize credentials, ssl handling etc.
        :param default_project: default project to use when fetching or executing flyte entities.
        :param default_domain: default domain to use when fetching or executing flyte entities.
        :param data_upload_location: this is where all the default data will be uploaded when providing inputs.
            The default location - `s3://my-s3-bucket/data` works for sandbox/demo environment. Please override this for non-sandbox cases.
        """
        if config is None or config.platform is None or config.platform.endpoint is None:
            raise user_exceptions.FlyteAssertion("Flyte endpoint should be provided.")

        self._client = SynchronousFlyteClient(config.platform, **kwargs)
        self._config = config
        # read config files, env vars, host, ssl options for admin client
        self._default_project = default_project
        self._default_domain = default_domain

        self._file_access = FileAccessProvider(
            local_sandbox_dir=os.path.join(config.local_sandbox_path, "control_plane_metadata"),
            raw_output_prefix=data_upload_location,
            data_config=config.data_config,
        )

        # Save the file access object locally, build a context for it and save that as well.
        self._ctx = FlyteContextManager.current_context().with_file_access(self._file_access).build()

    @property
    def context(self) -> FlyteContext:
        return self._ctx

    @property
    def client(self) -> SynchronousFlyteClient:
        """Return a SynchronousFlyteClient for additional operations."""
        return self._client

    @property
    def default_project(self) -> str:
        """Default project to use when fetching or executing flyte entities."""
        return self._default_project

    @property
    def default_domain(self) -> str:
        """Default project to use when fetching or executing flyte entities."""
        return self._default_domain

    @property
    def config(self) -> Config:
        """Image config."""
        return self._config

    @property
    def file_access(self) -> FileAccessProvider:
        """File access provider to use for offloading non-literal inputs/outputs."""
        return self._file_access

    def remote_context(self):
        """Context manager with remote-specific configuration."""
        return FlyteContextManager.with_context(
            FlyteContextManager.current_context().with_file_access(self.file_access)
        )

    def fetch_task(self, project: str = None, domain: str = None, name: str = None, version: str = None) -> FlyteTask:
        """Fetch a task entity from flyte admin.

        :param project: fetch entity from this project. If None, uses the default_project attribute.
        :param domain: fetch entity from this domain. If None, uses the default_domain attribute.
        :param name: fetch entity with matching name.
        :param version: fetch entity with matching version. If None, gets the latest version of the entity.
        :returns: :class:`~flytekit.remote.tasks.task.FlyteTask`

        :raises: FlyteAssertion if name is None
        """
        if name is None:
            raise user_exceptions.FlyteAssertion("the 'name' argument must be specified.")
        task_id = _get_entity_identifier(
            self.client.list_tasks_paginated,
            ResourceType.TASK,
            project or self.default_project,
            domain or self.default_domain,
            name,
            version,
        )
        admin_task = self.client.get_task(task_id)
        flyte_task = FlyteTask.promote_from_model(admin_task.closure.compiled_task.template)
        flyte_task._id = task_id
        return flyte_task

    def fetch_workflow(
        self, project: str = None, domain: str = None, name: str = None, version: str = None
    ) -> FlyteWorkflow:
        """Fetch a workflow entity from flyte admin.

        :param project: fetch entity from this project. If None, uses the default_project attribute.
        :param domain: fetch entity from this domain. If None, uses the default_domain attribute.
        :param name: fetch entity with matching name.
        :param version: fetch entity with matching version. If None, gets the latest version of the entity.
        :raises: FlyteAssertion if name is None
        """
        if name is None:
            raise user_exceptions.FlyteAssertion("the 'name' argument must be specified.")
        workflow_id = _get_entity_identifier(
            self.client.list_workflows_paginated,
            ResourceType.WORKFLOW,
            project or self.default_project,
            domain or self.default_domain,
            name,
            version,
        )
        admin_workflow = self.client.get_workflow(workflow_id)
        compiled_wf = admin_workflow.closure.compiled_workflow

        wf_templates = [compiled_wf.primary.template]
        wf_templates.extend([swf.template for swf in compiled_wf.sub_workflows])

        node_launch_plans = {}
        # TODO: Inspect branch nodes for launch plans
        for wf_template in wf_templates:
            for node in FlyteWorkflow.get_non_system_nodes(wf_template.nodes):
                if node.workflow_node is not None and node.workflow_node.launchplan_ref is not None:
                    lp_ref = node.workflow_node.launchplan_ref
                    if node.workflow_node.launchplan_ref not in node_launch_plans:
                        admin_launch_plan = self.client.get_launch_plan(lp_ref)
                        node_launch_plans[node.workflow_node.launchplan_ref] = admin_launch_plan.spec

        return FlyteWorkflow.promote_from_closure(compiled_wf, node_launch_plans)

    def fetch_launch_plan(
        self, project: str = None, domain: str = None, name: str = None, version: str = None
    ) -> FlyteLaunchPlan:
        """Fetch a launchplan entity from flyte admin.

        :param project: fetch entity from this project. If None, uses the default_project attribute.
        :param domain: fetch entity from this domain. If None, uses the default_domain attribute.
        :param name: fetch entity with matching name.
        :param version: fetch entity with matching version. If None, gets the latest version of the entity.
        :returns: :class:`~flytekit.remote.launch_plan.FlyteLaunchPlan`

        :raises: FlyteAssertion if name is None
        """
        if name is None:
            raise user_exceptions.FlyteAssertion("the 'name' argument must be specified.")
        launch_plan_id = _get_entity_identifier(
            self.client.list_launch_plans_paginated,
            ResourceType.LAUNCH_PLAN,
            project or self.default_project,
            domain or self.default_domain,
            name,
            version,
        )
        admin_launch_plan = self.client.get_launch_plan(launch_plan_id)
        flyte_launch_plan = FlyteLaunchPlan.promote_from_model(launch_plan_id, admin_launch_plan.spec)

        wf_id = flyte_launch_plan.workflow_id
        workflow = self.fetch_workflow(wf_id.project, wf_id.domain, wf_id.name, wf_id.version)
        flyte_launch_plan._interface = workflow.interface
        flyte_launch_plan._flyte_workflow = workflow

        return flyte_launch_plan

    def fetch_execution(self, project: str = None, domain: str = None, name: str = None) -> FlyteWorkflowExecution:
        """Fetch a workflow execution entity from flyte admin.

        :param project: fetch entity from this project. If None, uses the default_project attribute.
        :param domain: fetch entity from this domain. If None, uses the default_domain attribute.
        :param name: fetch entity with matching name.
        :returns: :class:`~flytekit.remote.workflow_execution.FlyteWorkflowExecution`

        :raises: FlyteAssertion if name is None
        """
        if name is None:
            raise user_exceptions.FlyteAssertion("the 'name' argument must be specified.")
        execution = FlyteWorkflowExecution.promote_from_model(
            self.client.get_execution(
                WorkflowExecutionIdentifier(
                    project or self.default_project,
                    domain or self.default_domain,
                    name,
                )
            )
        )
        return self.sync_execution(execution)

    ######################
    #  Listing Entities  #
    ######################

    def recent_executions(
        self,
        project: typing.Optional[str] = None,
        domain: typing.Optional[str] = None,
        limit: typing.Optional[int] = 100,
    ) -> typing.List[FlyteWorkflowExecution]:
        # Ignore token for now
        exec_models, _ = self.client.list_executions_paginated(
            project or self.default_project,
            domain or self.default_domain,
            limit,
            sort_by=MOST_RECENT_FIRST,
        )
        return [FlyteWorkflowExecution.promote_from_model(e) for e in exec_models]

    def list_tasks_by_version(
        self,
        version: str,
        project: typing.Optional[str] = None,
        domain: typing.Optional[str] = None,
        limit: typing.Optional[int] = 100,
    ) -> typing.List[FlyteTask]:
        if not version:
            raise ValueError("Must specify a version")

        named_entity_id = common_models.NamedEntityIdentifier(
            project=project or self.default_project,
            domain=domain or self.default_domain,
        )
        # Ignore token for now
        t_models, _ = self.client.list_tasks_paginated(
            named_entity_id,
            filters=[filter_models.Filter.from_python_std(f"eq(version,{version})")],
            limit=limit,
        )
        return [FlyteTask.promote_from_model(t.closure.compiled_task.template) for t in t_models]

    #####################
    # Register Entities #
    #####################

    def _resolve_identifier(self, t: int, name: str, version: str, ss: SerializationSettings) -> Identifier:
        ident = Identifier(
            resource_type=t,
            project=ss.project or self.default_project if ss else self.default_project,
            domain=ss.domain or self.default_domain if ss else self.default_domain,
            name=name,
            version=version or ss.version,
        )
        if not ident.project or not ident.domain or not ident.name or not ident.version:
            raise ValueError(
                f"To register a new {ident.resource_type}, (project, domain, name, version) required, "
                f"received ({ident.project}, {ident.domain}, {ident.name}, {ident.version})."
            )
        return ident

    def _serialize_and_register(
        self,
        entity: FlyteLocalEntity,
        settings: typing.Optional[SerializationSettings],
        version: str,
        options: typing.Optional[Options] = None,
    ) -> Identifier:
        """
        This method serializes and register the given Flyte entity
        :return: Identifier of the registered entity
        """
        m = OrderedDict()
        # Create dummy serialization settings for now.
        # TODO: Clean this up by using lazy usage of serialization settings in translator.py
        serialization_settings = (
            settings
            if settings
            else SerializationSettings(
                ImageConfig.auto_default_image(),
                project=self.default_project,
                domain=self.default_domain,
                version=version,
            )
        )
        _ = get_serializable(m, settings=serialization_settings, entity=entity, options=options)

        ident = None
        for entity, cp_entity in m.items():
            if isinstance(entity, RemoteEntity):
                remote_logger.debug(f"Skipping registration of remote entity: {entity.name}")
                continue
            if isinstance(
                cp_entity,
                (
                    workflow_model.Node,
                    workflow_model.WorkflowNode,
                    workflow_model.BranchNode,
                    workflow_model.TaskNode,
                ),
            ):
                remote_logger.debug("Ignoring nodes for registration.")
                continue
            elif isinstance(cp_entity, ReferenceSpec):
                remote_logger.debug(f"Skipping registration of Reference entity, name: {entity.name}")
                continue

            if not isinstance(cp_entity, admin_workflow_models.WorkflowSpec) and not settings:
                # Only in the case of workflows can we use the dummy serialization settings.
                raise user_exceptions.FlyteValueException(
                    settings,
                    f"No serialization settings set, but workflow contains entities that need to be "
                    f"registered. Type: {type(entity)} {entity.name}",
                )
            try:
                if isinstance(cp_entity, task_models.TaskSpec):
                    ident = self._resolve_identifier(ResourceType.TASK, entity.name, version, settings)
                    self.client.create_task(task_identifer=ident, task_spec=cp_entity)
                elif isinstance(cp_entity, admin_workflow_models.WorkflowSpec):
                    ident = self._resolve_identifier(ResourceType.WORKFLOW, entity.name, version, settings)
                    try:
                        self.client.create_workflow(workflow_identifier=ident, workflow_spec=cp_entity)
                    except FlyteEntityAlreadyExistsException:
                        remote_logger.info(f"{entity.name} already exists")
                    # Let us also create a default launch-plan, ideally the default launchplan should be added
                    # to the orderedDict, but we do not.
                    default_lp = LaunchPlan.get_default_launch_plan(self.context, entity)
                    lp_entity = get_serializable_launch_plan(
                        OrderedDict(),
                        settings or serialization_settings,
                        default_lp,
                        recurse_downstream=False,
                        options=options,
                    )
                    self.client.create_launch_plan(lp_entity.id, lp_entity.spec)
                elif isinstance(cp_entity, launch_plan_models.LaunchPlan):
                    ident = self._resolve_identifier(ResourceType.LAUNCH_PLAN, entity.name, version, settings)
                    self.client.create_launch_plan(launch_plan_identifer=ident, launch_plan_spec=cp_entity.spec)
                else:
                    raise AssertionError(f"Unknown entity of type {type(cp_entity)}")
            except FlyteEntityAlreadyExistsException:
                remote_logger.info(f"{entity.name} already exists")
            except Exception as e:
                remote_logger.info(f"Failed to register entity {entity.name} with error {e}")
                raise
        return ident

    def register_task(
        self, entity: PythonTask, serialization_settings: SerializationSettings, version: typing.Optional[str] = None
    ) -> FlyteTask:
        """
        Register a qualified task (PythonTask) with Remote
        For any conflicting parameters method arguments are regarded as overrides

        :param entity: PythonTask can be either @task or a instance of a Task class
        :param serialization_settings:  Settings that will be used to override various serialization parameters.
        :param version: version that will be used to register. If not specified will default to using the serialization settings default
        :return:
        """
        ident = self._serialize_and_register(entity=entity, settings=serialization_settings, version=version)
        ft = self.fetch_task(
            ident.project,
            ident.domain,
            ident.name,
            ident.version,
        )
        ft._python_interface = entity.python_interface
        return ft

    def register_workflow(
        self,
        entity: WorkflowBase,
        serialization_settings: typing.Optional[SerializationSettings] = None,
        version: typing.Optional[str] = None,
        default_launch_plan: typing.Optional[bool] = True,
        options: typing.Optional[Options] = None,
    ) -> FlyteWorkflow:
        """
        Use this method to register a workflow.
        :param version: version for the entity to be registered as
        :param entity: The workflow to be registered
        :param serialization_settings: The serialization settings to be used
        :param default_launch_plan: This should be true if a default launch plan should be created for the workflow
        :param options: Additional execution options that can be configured for the default launchplan
        :return:
        """
        ident = self._resolve_identifier(ResourceType.WORKFLOW, entity.name, version, serialization_settings)
        if serialization_settings:
            b = serialization_settings.new_builder()
            b.project = ident.project
            b.domain = ident.domain
            b.version = ident.version
            serialization_settings = b.build()
        ident = self._serialize_and_register(entity, serialization_settings, version, options)
        if default_launch_plan:
            default_lp = LaunchPlan.get_default_launch_plan(self.context, entity)
            self.register_launch_plan(
                default_lp, version=ident.version, project=ident.project, domain=ident.domain, options=options
            )
            remote_logger.debug("Created default launch plan for Workflow")

        fwf = self.fetch_workflow(ident.project, ident.domain, ident.name, ident.version)
        fwf._python_interface = entity.python_interface
        return fwf

    def register_script(
        self,
        entity: WorkflowBase,
        image_config: typing.Optional[ImageConfig] = None,
        version: typing.Optional[str] = None,
        project: typing.Optional[str] = None,
        domain: typing.Optional[str] = None,
        destination_dir: str = ".",
        default_launch_plan: typing.Optional[bool] = True,
        options: typing.Optional[Options] = None,
    ) -> FlyteWorkflow:
        """
        Use this method to register a workflow via script mode.
        :param destination_dir:
        :param domain:
        :param project:
        :param image_config:
        :param version: version for the entity to be registered as
        :param entity: The workflow to be registered
        :param default_launch_plan: This should be true if a default launch plan should be created for the workflow
        :param options: Additional execution options that can be configured for the default launchplan
        :return:
        """
        _, _, _, fname = tracker.extract_task_module(entity)

        if image_config is None:
            image_config = ImageConfig.auto_default_image()

        upload_location, md5_bytes = fast_register_single_script(
            entity,
            functools.partial(
                self.client.get_upload_signed_url,
                project=project or self.default_project,
                domain=domain or self.default_domain,
                filename="scriptmode.tar.gz",
            ),
        )

        serialization_settings = SerializationSettings(
            project=project,
            domain=domain,
            image_config=image_config,
            fast_serialization_settings=FastSerializationSettings(
                enabled=True,
                destination_dir=destination_dir,
                distribution_location=upload_location.native_url,
            ),
        )

        if version is None:
            # The md5 version that we send to S3/GCS has to match the file contents exactly,
            # but we don't have to use it when registering with the Flyte backend.
            # For that add the hash of the compilation settings to hash of file
            from flytekit import __version__

            h = hashlib.md5(md5_bytes)
            h.update(bytes(serialization_settings.to_json(), "utf-8"))
            h.update(bytes(__version__, "utf-8"))
            version = base64.urlsafe_b64encode(h.digest())

        return self.register_workflow(entity, serialization_settings, version, default_launch_plan, options)

    def register_launch_plan(
        self,
        entity: LaunchPlan,
        version: str,
        project: typing.Optional[str] = None,
        domain: typing.Optional[str] = None,
        options: typing.Optional[Options] = None,
    ) -> FlyteLaunchPlan:
        """
        Register a given launchplan, possibly applying overrides from the provided options.
        :param entity: Launchplan to be registered
        :param version:
        :param project: Optionally provide a project, if not already provided in flyteremote constructor or a separate one
        :param domain: Optionally provide a domain, if not already provided in FlyteRemote constructor or a separate one
        :param options:
        :return:
        """
        ss = SerializationSettings(image_config=ImageConfig(), project=project, domain=domain, version=version)

        ident = self._resolve_identifier(ResourceType.LAUNCH_PLAN, entity.name, version, ss)
        m = OrderedDict()
        idl_lp = get_serializable_launch_plan(m, ss, entity, recurse_downstream=False, options=options)
        try:
            self.client.create_launch_plan(ident, idl_lp.spec)
        except FlyteEntityAlreadyExistsException:
            remote_logger.debug("Launchplan already exists, ignoring")
        flp = self.fetch_launch_plan(ident.project, ident.domain, ident.name, ident.version)
        flp._python_interface = entity.python_interface
        return flp

    ####################
    # Execute Entities #
    ####################

    def _execute(
        self,
        entity: typing.Union[FlyteTask, FlyteWorkflow, FlyteLaunchPlan],
        inputs: typing.Dict[str, typing.Any],
        project: str = None,
        domain: str = None,
        execution_name: str = None,
        options: typing.Optional[Options] = None,
        wait: bool = False,
        type_hints: typing.Optional[typing.Dict[str, typing.Type]] = None,
    ) -> FlyteWorkflowExecution:
        """Common method for execution across all entities.

        :param flyte_id: entity identifier
        :param inputs: dictionary mapping argument names to values
        :param project: project on which to execute the entity referenced by flyte_id
        :param domain: domain on which to execute the entity referenced by flyte_id
        :param execution_name: name of the execution
        :param wait: if True, waits for execution to complete
        :param type_hints: map of python types to inputs so that the TypeEngine knows how to convert the input values
          into Flyte Literals.
        :returns: :class:`~flytekit.remote.workflow_execution.FlyteWorkflowExecution`
        """
        execution_name = execution_name or "f" + uuid.uuid4().hex[:19]
        if not options:
            options = Options()
        if options.disable_notifications is not None:
            if options.disable_notifications:
                notifications = None
            else:
                notifications = NotificationList(options.notifications)
        else:
            notifications = NotificationList([])

        type_hints = type_hints or {}
        literal_map = {}
        with self.remote_context() as ctx:
            input_flyte_type_map = entity.interface.inputs

            for k, v in inputs.items():
                if input_flyte_type_map.get(k) is None:
                    raise user_exceptions.FlyteValueException(
                        k, f"The {entity.__class__.__name__} doesn't have this input key."
                    )
                if isinstance(v, Literal):
                    lit = v
                else:
                    if k not in type_hints:
                        try:
                            type_hints[k] = TypeEngine.guess_python_type(input_flyte_type_map[k].type)
                        except ValueError:
                            remote_logger.debug(f"Could not guess type for {input_flyte_type_map[k].type}, skipping...")
                    variable = entity.interface.inputs.get(k)
                    hint = type_hints[k]
                    lit = TypeEngine.to_literal(ctx, v, hint, variable.type)
                literal_map[k] = lit

            literal_inputs = literal_models.LiteralMap(literals=literal_map)

        try:
            # Currently, this will only execute the flyte entity referenced by
            # flyte_id in the same project and domain. However, it is possible to execute it in a different project
            # and domain, which is specified in the first two arguments of client.create_execution. This is useful
            # in the case that I want to use a flyte entity from e.g. project "A" but actually execute the entity on a
            # different project "B". For now, this method doesn't support this use case.
            exec_id = self.client.create_execution(
                project or self.default_project,
                domain or self.default_domain,
                execution_name,
                ExecutionSpec(
                    entity.id,
                    ExecutionMetadata(
                        ExecutionMetadata.ExecutionMode.MANUAL,
                        "placeholder",  # Admin replaces this from oidc token if auth is enabled.
                        0,
                    ),
                    notifications=notifications,
                    disable_all=options.disable_notifications,
                    labels=options.labels,
                    annotations=options.annotations,
                    raw_output_data_config=options.raw_output_data_config,
                    auth_role=None,
                    max_parallelism=options.max_parallelism,
                    security_context=options.security_context,
                ),
                literal_inputs,
            )
        except user_exceptions.FlyteEntityAlreadyExistsException:
            remote_logger.warning(
                f"Execution with Execution ID {execution_name} already exists. "
                f"Assuming this is the same execution, returning!"
            )
            exec_id = WorkflowExecutionIdentifier(
                project=project or self.default_project, domain=domain or self.default_domain, name=execution_name
            )
        execution = FlyteWorkflowExecution.promote_from_model(self.client.get_execution(exec_id))

        if wait:
            return self.wait(execution)
        return execution

    def _resolve_identifier_kwargs(
        self,
        entity: typing.Any,
        project: str,
        domain: str,
        name: str,
        version: str,
    ) -> ResolvedIdentifiers:
        """
        Resolves the identifier attributes based on user input, falling back on the default project/domain and
        auto-generated version, and ultimately the entity project/domain if entity is a remote flyte entity.
        """
        ident = ResolvedIdentifiers(
            project=project or self.default_project,
            domain=domain or self.default_domain,
            name=name or entity.name,
            version=version,
        )
        if not (ident.project and ident.domain and ident.name):
            raise ValueError(
                f"Cannot launch an execution with missing project/domain/name {ident} for entity type {type(entity)}."
                f" Specify them in the execute method or when intializing FlyteRemote"
            )
        return ident

    def execute(
        self,
        entity: typing.Union[FlyteTask, FlyteLaunchPlan, FlyteWorkflow, PythonTask, WorkflowBase, LaunchPlan],
        inputs: typing.Dict[str, typing.Any],
        project: str = None,
        domain: str = None,
        name: str = None,
        version: str = None,
        execution_name: str = None,
        image_config: typing.Optional[ImageConfig] = None,
        options: typing.Optional[Options] = None,
        wait: bool = False,
        type_hints: typing.Optional[typing.Dict[str, typing.Type]] = None,
    ) -> FlyteWorkflowExecution:
        """
        Execute a task, workflow, or launchplan, either something that's been declared locally, or a fetched entity.

        This method supports:
        - ``Flyte{Task, Workflow, LaunchPlan}`` remote module objects.
        - ``@task``-decorated functions and ``TaskTemplate`` tasks.
        - ``@workflow``-decorated functions.
        - ``LaunchPlan`` objects.

        For local entities, this code will attempt to find the entity first, and if missing, will compile and register
        the object.

        Not all arguments are relevant in all circumstances. For example, there's no reason to use the serialization
        settings for entities that have already been registered on Admin.

        :param options:
        :param entity: entity to execute
        :param inputs: dictionary mapping argument names to values
        :param project: execute entity in this project. If entity doesn't exist in the project, register the entity
            first before executing.
        :param domain: execute entity in this domain. If entity doesn't exist in the domain, register the entity
            first before executing.
        :param name: execute entity using this name. If not None, use this value instead of ``entity.name``
        :param version: execute entity using this version. If None, uses auto-generated value.
        :param execution_name: name of the execution. If None, uses auto-generated value.
        :param image_config:
        :param wait: if True, waits for execution to complete
        :param type_hints: Python types to be passed to the TypeEngine so that it knows how to properly convert the
          input values for the execution into Flyte literals. If missing, will default to first guessing the type
          using the type engine, and then to ``type(v)``. Providing the correct Python types is particularly important
          if the inputs are containers like lists or maps, or if the Python type is one of the more complex Flyte
          provided classes (like a StructuredDataset that's annotated with columns).

        .. note:

            The ``name`` and ``version`` arguments do not apply to ``FlyteTask``, ``FlyteLaunchPlan``, and
            ``FlyteWorkflow`` entity inputs. These values are determined by referencing the entity identifier values.
        """
        if entity.python_interface:
            type_hints = type_hints or entity.python_interface.inputs
        if isinstance(entity, FlyteTask) or isinstance(entity, FlyteLaunchPlan):
            return self.execute_remote_task_lp(
                entity=entity,
                inputs=inputs,
                project=project,
                domain=domain,
                execution_name=execution_name,
                options=options,
                wait=wait,
                type_hints=type_hints,
            )
        if isinstance(entity, FlyteWorkflow):
            return self.execute_remote_wf(
                entity=entity,
                inputs=inputs,
                project=project,
                domain=domain,
                execution_name=execution_name,
                options=options,
                wait=wait,
                type_hints=type_hints,
            )
        if isinstance(entity, PythonTask):
            return self.execute_local_task(
                entity=entity,
                inputs=inputs,
                project=project,
                domain=domain,
                name=name,
                version=version,
                execution_name=execution_name,
                image_config=image_config,
                wait=wait,
            )
        if isinstance(entity, WorkflowBase):
            return self.execute_local_workflow(
                entity=entity,
                inputs=inputs,
                project=project,
                domain=domain,
                name=name,
                version=version,
                execution_name=execution_name,
                image_config=image_config,
                options=options,
                wait=wait,
            )
        if isinstance(entity, LaunchPlan):
            return self.execute_local_launch_plan(
                entity=entity,
                inputs=inputs,
                version=version,
                project=project,
                domain=domain,
                execution_name=execution_name,
                options=options,
                wait=wait,
            )
        raise NotImplementedError(f"entity type {type(entity)} not recognized for execution")

    # Flyte Remote Entities
    # ---------------------

    def execute_remote_task_lp(
        self,
        entity: typing.Union[FlyteTask, FlyteLaunchPlan],
        inputs: typing.Dict[str, typing.Any],
        project: str = None,
        domain: str = None,
        execution_name: str = None,
        options: typing.Optional[Options] = None,
        wait: bool = False,
        type_hints: typing.Optional[typing.Dict[str, typing.Type]] = None,
    ) -> FlyteWorkflowExecution:
        """Execute a FlyteTask, or FlyteLaunchplan.

        NOTE: the name and version arguments are currently not used and only there consistency in the function signature
        """
        return self._execute(
            entity,
            inputs,
            project=project,
            domain=domain,
            execution_name=execution_name,
            wait=wait,
            options=options,
            type_hints=type_hints,
        )

    def execute_remote_wf(
        self,
        entity: FlyteWorkflow,
        inputs: typing.Dict[str, typing.Any],
        project: str = None,
        domain: str = None,
        execution_name: str = None,
        options: typing.Optional[Options] = None,
        wait: bool = False,
        type_hints: typing.Optional[typing.Dict[str, typing.Type]] = None,
    ) -> FlyteWorkflowExecution:
        """Execute a FlyteWorkflow.

        NOTE: the name and version arguments are currently not used and only there consistency in the function signature
        """
        launch_plan = self.fetch_launch_plan(entity.id.project, entity.id.domain, entity.id.name, entity.id.version)
        return self.execute_remote_task_lp(
            launch_plan,
            inputs,
            project=project,
            domain=domain,
            execution_name=execution_name,
            options=options,
            wait=wait,
            type_hints=type_hints,
        )

    # Flytekit Entities
    # -----------------

    def execute_local_task(
        self,
        entity: PythonTask,
        inputs: typing.Dict[str, typing.Any],
        project: str = None,
        domain: str = None,
        name: str = None,
        version: str = None,
        execution_name: str = None,
        image_config: typing.Optional[ImageConfig] = None,
        wait: bool = False,
    ) -> FlyteWorkflowExecution:
        """
        Execute an @task-decorated function or TaskTemplate task.

        :param entity:
        :param inputs:
          register the task, which requires compiling the task, before running it.
        :param project:
        :param domain:
        :param name:
        :param version:
        :param execution_name:
        :param image_config:
        :param wait:
        :return:
        """
        resolved_identifiers = self._resolve_identifier_kwargs(entity, project, domain, name, version)
        resolved_identifiers_dict = asdict(resolved_identifiers)
        try:
            flyte_task: FlyteTask = self.fetch_task(**resolved_identifiers_dict)
        except FlyteEntityNotExistException:
            if isinstance(entity, PythonAutoContainerTask):
                if not image_config:
                    raise ValueError(f"PythonTask {entity.name} not already registered, but image_config missing")
            ss = SerializationSettings(
                image_config=image_config,
                project=project or self.default_project,
                domain=domain or self._default_domain,
                version=version,
            )
            flyte_task: FlyteTask = self.register_task(entity, ss)

        return self.execute(
            flyte_task,
            inputs,
            project=resolved_identifiers.project,
            domain=resolved_identifiers.domain,
            execution_name=execution_name,
            wait=wait,
            type_hints=entity.python_interface.inputs,
        )

    def execute_local_workflow(
        self,
        entity: WorkflowBase,
        inputs: typing.Dict[str, typing.Any],
        project: str = None,
        domain: str = None,
        name: str = None,
        version: str = None,
        execution_name: str = None,
        image_config: typing.Optional[ImageConfig] = None,
        options: typing.Optional[Options] = None,
        wait: bool = False,
    ) -> FlyteWorkflowExecution:
        """
        Execute an @workflow decorated function.
        :param entity:
        :param inputs:
        :param project:
        :param domain:
        :param name:
        :param version:
        :param execution_name:
        :param image_config:
        :param options:
        :param wait:
        :return:
        """
        resolved_identifiers = self._resolve_identifier_kwargs(entity, project, domain, name, version)
        resolved_identifiers_dict = asdict(resolved_identifiers)

        ss = SerializationSettings(
            image_config=image_config,
            project=resolved_identifiers.project,
            domain=resolved_identifiers.domain,
            version=resolved_identifiers.version,
        )
        try:
            # Just fetch to see if it already exists
            # todo: Add logic to check that the fetched workflow is functionally equivalent.
            self.fetch_workflow(**resolved_identifiers_dict)
        except FlyteEntityNotExistException:
            remote_logger.info("Registering workflow because it wasn't found in Flyte Admin.")
            if not image_config:
                raise ValueError("Need image config since we are registering")
            self.register_workflow(entity, ss, version=version, options=options)

        try:
            flyte_lp = self.fetch_launch_plan(**resolved_identifiers_dict)
        except FlyteEntityNotExistException:
            remote_logger.info("Try to register default launch plan because it wasn't found in Flyte Admin!")
            default_lp = LaunchPlan.get_default_launch_plan(self.context, entity)
            self.register_launch_plan(
                default_lp,
                project=resolved_identifiers.project,
                domain=resolved_identifiers.domain,
                version=version,
                options=options,
            )
            flyte_lp = self.fetch_launch_plan(**resolved_identifiers_dict)

        return self.execute(
            flyte_lp,
            inputs,
            project=project,
            domain=domain,
            execution_name=execution_name,
            wait=wait,
            options=options,
            type_hints=entity.python_interface.inputs,
        )

    def execute_local_launch_plan(
        self,
        entity: LaunchPlan,
        inputs: typing.Dict[str, typing.Any],
        version: str,
        project: typing.Optional[str] = None,
        domain: typing.Optional[str] = None,
        execution_name: typing.Optional[str] = None,
        options: typing.Optional[Options] = None,
        wait: bool = False,
    ) -> FlyteWorkflowExecution:
        """

        :param entity: The locally defined launch plan object
        :param inputs: Inputs to be passed into the execution as a dict with Python native values.
        :param version: The version to look up/register the launch plan (if not already exists)
        :param project: The same as version, but will default to the Remote object's project
        :param domain: The same as version, but will default to the Remote object's domain
        :param execution_name: If specified, will be used as the execution name instead of randomly generating.
        :param options:
        :param wait:
        :return:
        """
        try:
            flyte_launchplan: FlyteLaunchPlan = self.fetch_launch_plan(
                project=project,
                domain=domain,
                name=entity.name,
                version=version,
            )
        except FlyteEntityNotExistException:
            flyte_launchplan: FlyteLaunchPlan = self.register_launch_plan(
                entity,
                version=version,
                project=project,
                domain=domain,
            )
        return self.execute_remote_task_lp(
            flyte_launchplan,
            inputs,
            project=project,
            domain=domain,
            execution_name=execution_name,
            options=options,
            wait=wait,
            type_hints=entity.python_interface.inputs,
        )

    ###################################
    # Wait for Executions to Complete #
    ###################################

    def wait(
        self,
        execution: FlyteWorkflowExecution,
        timeout: typing.Optional[timedelta] = None,
        poll_interval: typing.Optional[timedelta] = None,
        sync_nodes: bool = True,
    ) -> FlyteWorkflowExecution:
        """Wait for an execution to finish.

        :param execution: execution object to wait on
        :param timeout: maximum amount of time to wait
        :param poll_interval: sync workflow execution at this interval
        :param sync_nodes: passed along to the sync call for the workflow execution
        """
        poll_interval = poll_interval or timedelta(seconds=30)
        time_to_give_up = datetime.max if timeout is None else datetime.utcnow() + timeout

        while datetime.utcnow() < time_to_give_up:
            execution = self.sync_execution(execution, sync_nodes=sync_nodes)
            if execution.is_done:
                return execution
            time.sleep(poll_interval.total_seconds())

        raise user_exceptions.FlyteTimeout(f"Execution {self} did not complete before timeout.")

    ########################
    # Sync Execution State #
    ########################

    def sync(
        self,
        execution: FlyteWorkflowExecution,
        entity_definition: typing.Union[FlyteWorkflow, FlyteTask] = None,
        sync_nodes: bool = False,
    ) -> FlyteWorkflowExecution:
        """
        This function was previously a singledispatchmethod. We've removed that but this function remains
        so that we don't break people.

        :param execution:
        :param entity_definition:
        :param sync_nodes: By default sync will fetch data on all underlying node executions (recursively,
          so subworkflows will also get picked up). Set this to False in order to prevent that (which
          will make this call faster).
        :return: Returns the same execution object, but with additional information pulled in.
        """
        if not isinstance(execution, FlyteWorkflowExecution):
            raise ValueError(f"remote.sync should only be called on workflow executions, got {type(execution)}")
        return self.sync_execution(execution, entity_definition, sync_nodes)

    def sync_execution(
        self,
        execution: FlyteWorkflowExecution,
        entity_definition: typing.Union[FlyteWorkflow, FlyteTask] = None,
        sync_nodes: bool = False,
    ) -> FlyteWorkflowExecution:
        """
        Sync a FlyteWorkflowExecution object with its corresponding remote state.
        """
        if entity_definition is not None:
            raise ValueError("Entity definition arguments aren't supported when syncing workflow executions")

        # Update closure, and then data, because we don't want the execution to finish between when we get the data,
        # and then for the closure to have is_done to be true.
        execution._closure = self.client.get_execution(execution.id).closure
        execution_data = self.client.get_execution_data(execution.id)
        lp_id = execution.spec.launch_plan
        underlying_node_executions = []
        if sync_nodes:
            underlying_node_executions = [
                FlyteNodeExecution.promote_from_model(n) for n in iterate_node_executions(self.client, execution.id)
            ]

        # This condition is only true for single-task executions
        if execution.spec.launch_plan.resource_type == ResourceType.TASK:
            flyte_entity = self.fetch_task(lp_id.project, lp_id.domain, lp_id.name, lp_id.version)
            node_interface = flyte_entity.interface
            if sync_nodes:
                # Need to construct the mapping. There should've been returned exactly three nodes, a start,
                # an end, and a task node.
                task_node_exec = [
                    x
                    for x in filter(
                        lambda x: x.id.node_id != constants.START_NODE_ID and x.id.node_id != constants.END_NODE_ID,
                        underlying_node_executions,
                    )
                ]
                # We need to manually make a map of the nodes since there is none for single task executions
                # Assume the first one is the only one.
                node_mapping = (
                    {
                        task_node_exec[0].id.node_id: FlyteNode(
                            id=flyte_entity.id,
                            upstream_nodes=[],
                            bindings=[],
                            metadata=NodeMetadata(name=""),
                            flyte_task=flyte_entity,
                        )
                    }
                    if len(task_node_exec) >= 1
                    else {}  # This is for the case where node executions haven't appeared yet
                )
        # This is the default case, an execution of a normal workflow through a launch plan
        else:
            fetched_lp = self.fetch_launch_plan(lp_id.project, lp_id.domain, lp_id.name, lp_id.version)
            node_interface = fetched_lp.flyte_workflow.interface
            execution._flyte_workflow = fetched_lp.flyte_workflow
            node_mapping = fetched_lp.flyte_workflow._node_map

        # update node executions (if requested), and inputs/outputs
        if sync_nodes:
            node_execs = {}
            for n in underlying_node_executions:
                node_execs[n.id.node_id] = self.sync_node_execution(n, node_mapping)  # noqa
            execution._node_executions = node_execs
        return self._assign_inputs_and_outputs(execution, execution_data, node_interface)

    def sync_node_execution(
        self,
        execution: FlyteNodeExecution,
        node_mapping: typing.Dict[str, FlyteNode],
    ) -> FlyteNodeExecution:
        """
        Get data backing a node execution. These FlyteNodeExecution objects should've come from Admin with the model
        fields already populated correctly. For purposes of the remote experience, we'd like to supplement the object
        with some additional fields:
          - inputs/outputs
          - task/workflow executions, and/or underlying node executions in the case of parent nodes
          - TypedInterface (remote wrapper type)

        A node can have several different types of executions behind it. That is, the node could've run (perhaps
        multiple times because of retries):
          - A task
          - A static subworkflow
          - A dynamic subworkflow (which in turn may have run additional tasks, subwfs, and/or launch plans)
          - A launch plan

        The data model is complicated, so ascertaining which of these happened is a bit tricky. That logic is
        encapsulated in this function.
        """
        # For single task execution - the metadata spec node id is missing. In these cases, revert to regular node id
        node_id = execution.metadata.spec_node_id
        # This case supports single-task execution compiled workflows.
        if node_id and node_id not in node_mapping and execution.id.node_id in node_mapping:
            node_id = execution.id.node_id
            remote_logger.debug(
                f"Using node execution ID {node_id} instead of spec node id "
                f"{execution.metadata.spec_node_id}, single-task execution likely."
            )
        # This case supports single-task execution compiled workflows with older versions of admin/propeller
        if not node_id:
            node_id = execution.id.node_id
            remote_logger.debug(f"No metadata spec_node_id found, using {node_id}")

        # First see if it's a dummy node, if it is, we just skip it.
        if constants.START_NODE_ID in node_id or constants.END_NODE_ID in node_id:
            return execution

        # Look for the Node object in the mapping supplied
        if node_id in node_mapping:
            execution._node = node_mapping[node_id]
        else:
            raise Exception(f"Missing node from mapping: {node_id}")

        # Get the node execution data
        node_execution_get_data_response = self.client.get_node_execution_data(execution.id)

        # Calling a launch plan directly case
        # If a node ran a launch plan directly (i.e. not through a dynamic task or anything) then
        # the closure should have a workflow_node_metadata populated with the launched execution id.
        # The parent node flag should not be populated here
        # This is the simplest case
        if not execution.metadata.is_parent_node and execution.closure.workflow_node_metadata:
            launched_exec_id = execution.closure.workflow_node_metadata.execution_id
            # This is a recursive call, basically going through the same process that brought us here in the first
            # place, but on the launched execution.
            launched_exec = self.fetch_execution(
                project=launched_exec_id.project, domain=launched_exec_id.domain, name=launched_exec_id.name
            )
            self.sync_execution(launched_exec)
            if launched_exec.is_done:
                # The synced underlying execution should've had these populated.
                execution._inputs = launched_exec.inputs
                execution._outputs = launched_exec.outputs
            execution._workflow_executions.append(launched_exec)
            execution._interface = launched_exec._flyte_workflow.interface
            return execution

        # If a node ran a static subworkflow or a dynamic subworkflow then the parent flag will be set.
        if execution.metadata.is_parent_node:
            # We'll need to query child node executions regardless since this is a parent node
            child_node_executions = iterate_node_executions(
                self.client,
                workflow_execution_identifier=execution.id.execution_id,
                unique_parent_id=execution.id.node_id,
            )
            child_node_executions = [x for x in child_node_executions]

            # If this was a dynamic task, then there should be a CompiledWorkflowClosure inside the
            # NodeExecutionGetDataResponse
            if node_execution_get_data_response.dynamic_workflow is not None:
                compiled_wf = node_execution_get_data_response.dynamic_workflow.compiled_workflow
                node_launch_plans = {}
                # TODO: Inspect branch nodes for launch plans
                for node in FlyteWorkflow.get_non_system_nodes(compiled_wf.primary.template.nodes):
                    if (
                        node.workflow_node is not None
                        and node.workflow_node.launchplan_ref is not None
                        and node.workflow_node.launchplan_ref not in node_launch_plans
                    ):
                        node_launch_plans[node.workflow_node.launchplan_ref] = self.client.get_launch_plan(
                            node.workflow_node.launchplan_ref
                        ).spec

                dynamic_flyte_wf = FlyteWorkflow.promote_from_closure(compiled_wf, node_launch_plans)
                execution._underlying_node_executions = [
                    self.sync_node_execution(FlyteNodeExecution.promote_from_model(cne), dynamic_flyte_wf._node_map)
                    for cne in child_node_executions
                ]
                # This is copied from below - dynamic tasks have both task executions (executions of the parent
                # task) as well as underlying node executions (of the generated subworkflow). Feel free to refactor
                # if you can think of a better way.
                execution._task_executions = [
                    self.sync_task_execution(FlyteTaskExecution.promote_from_model(t))
                    for t in iterate_task_executions(self.client, execution.id)
                ]
                execution._interface = dynamic_flyte_wf.interface

            # Handle the case where it's a static subworkflow
            elif isinstance(execution._node.flyte_entity, FlyteWorkflow):
                sub_flyte_workflow = execution._node.flyte_entity
                sub_node_mapping = {n.id: n for n in sub_flyte_workflow.flyte_nodes}
                execution._underlying_node_executions = [
                    self.sync_node_execution(FlyteNodeExecution.promote_from_model(cne), sub_node_mapping)
                    for cne in child_node_executions
                ]
                execution._interface = sub_flyte_workflow.interface

            # Handle the case where it's a branch node
            elif execution._node.branch_node is not None:
                remote_logger.info(
                    "Skipping branch node execution for now - branch nodes will "
                    "not have inputs and outputs filled in"
                )
                return execution
            else:
                remote_logger.error(f"NE {execution} undeterminable, {type(execution._node)}, {execution._node}")
                raise Exception(f"Node execution undeterminable, entity has type {type(execution._node)}")

        # This is the plain ol' task execution case
        else:
            execution._task_executions = [
                self.sync_task_execution(FlyteTaskExecution.promote_from_model(t))
                for t in iterate_task_executions(self.client, execution.id)
            ]
            execution._interface = execution._node.flyte_entity.interface

        self._assign_inputs_and_outputs(
            execution,
            node_execution_get_data_response,
            execution.interface,
        )

        return execution

    def sync_task_execution(
        self, execution: FlyteTaskExecution, entity_definition: typing.Union[FlyteWorkflow, FlyteTask] = None
    ) -> FlyteTaskExecution:
        """Sync a FlyteTaskExecution object with its corresponding remote state."""
        if entity_definition is not None:
            raise ValueError("Entity definition arguments aren't supported when syncing task executions")

        execution._closure = self.client.get_task_execution(execution.id).closure
        execution_data = self.client.get_task_execution_data(execution.id)
        task_id = execution.id.task_id
        task = self.fetch_task(task_id.project, task_id.domain, task_id.name, task_id.version)
        return self._assign_inputs_and_outputs(execution, execution_data, task.interface)

    #############################
    # Terminate Execution State #
    #############################

    def terminate(self, execution: FlyteWorkflowExecution, cause: str):
        """Terminate a workflow execution.

        :param execution: workflow execution to terminate
        :param cause: reason for termination
        """
        self.client.terminate_execution(execution.id, cause)

    ##################
    # Helper Methods #
    ##################

    def _assign_inputs_and_outputs(
        self,
        execution: typing.Union[FlyteWorkflowExecution, FlyteNodeExecution, FlyteTaskExecution],
        execution_data,
        interface: TypedInterface,
    ):
        """Helper for assigning synced inputs and outputs to an execution object."""
        input_literal_map = self._get_input_literal_map(execution_data)
        execution._inputs = LiteralsResolver(input_literal_map.literals, interface.inputs, self.context)

        if execution.is_done and not execution.error:
            output_literal_map = self._get_output_literal_map(execution_data)
            execution._outputs = LiteralsResolver(output_literal_map.literals, interface.outputs, self.context)
        return execution

    def _get_input_literal_map(self, execution_data: ExecutionDataResponse) -> literal_models.LiteralMap:
        # Inputs are returned inline unless they are too big, in which case a url blob pointing to them is returned.
        if bool(execution_data.full_inputs.literals):
            return execution_data.full_inputs
        elif execution_data.inputs.bytes > 0:
            with self.remote_context() as ctx:
                tmp_name = os.path.join(ctx.file_access.local_sandbox_dir, "inputs.pb")
                ctx.file_access.get_data(execution_data.inputs.url, tmp_name)
                return literal_models.LiteralMap.from_flyte_idl(
                    utils.load_proto_from_file(literals_pb2.LiteralMap, tmp_name)
                )
        return literal_models.LiteralMap({})

    def _get_output_literal_map(self, execution_data: ExecutionDataResponse) -> literal_models.LiteralMap:
        # Outputs are returned inline unless they are too big, in which case a url blob pointing to them is returned.
        if bool(execution_data.full_outputs.literals):
            return execution_data.full_outputs
        elif execution_data.outputs.bytes > 0:
            with self.remote_context() as ctx:
                tmp_name = os.path.join(ctx.file_access.local_sandbox_dir, "outputs.pb")
                ctx.file_access.get_data(execution_data.outputs.url, tmp_name)
                return literal_models.LiteralMap.from_flyte_idl(
                    utils.load_proto_from_file(literals_pb2.LiteralMap, tmp_name)
                )
        return literal_models.LiteralMap({})

    def generate_http_domain(self) -> str:
        """
        This should generate the domain where the HTTP endpoints for the Flyte backend are hosted. This should be
        the domain that console is hosted on.

        :return:
        """
        protocol = "http" if self.config.platform.insecure else "https"
        endpoint = self.config.platform.endpoint
        # N.B.: this assumes that in case we have an identical configuration as the sandbox default config we are running single binary. The intent here is
        # to ensure that the urls produced in the getting started guide point to the correct place.
        if self.config.platform == Config.for_sandbox().platform:
            endpoint = "localhost:30080"
        return protocol + f"://{endpoint}"

    def generate_console_url(
        self, execution: typing.Union[FlyteWorkflowExecution, FlyteNodeExecution, FlyteTaskExecution]
    ):
        return f"{self.generate_http_domain()}/console/projects/{execution.id.project}/domains/{execution.id.domain}/executions/{execution.id.name}"
