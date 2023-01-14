import logging
import copy
from katatachi.worker import WorkerConfigStore, WorkerCache, WorkerMetadata
from katatachi.mod_view import NamedModViewColumn, ModViewQuery, ModViewStore
from katatachi.contrib.mod_view.update_one_button import UpdateOneButton
from katatachi.interface.mod_view.column_render import ButtonAfterCallbackBehavior
from .pipeline import Pipeline
from .pipeline_mod_view import PipelineModViewToState
from .pipeline_state import StateKey

logger = logging.getLogger(__name__)


def configure_pipeline_workers(
        pipeline: Pipeline,
        worker_config_store: WorkerConfigStore,
        worker_cache: WorkerCache,
):
    logger.info("Configuring pipeline workers")

    # DO NOT CHANGE pipeline namespace, otherwise reconciliation won't find existing workers
    pipeline_namespace = f"pipeline.{pipeline.name}"
    actual_workers = worker_config_store.get_all(namespace=pipeline_namespace)
    desired_worker_ids = set()

    for pipeline_worker in pipeline.workers:
        worker_id = f"{pipeline_namespace}.{pipeline_worker.name}"

        # Register pipeline worker
        worker_cache.register_pipeline_worker(
            worker_id=worker_id, func=pipeline_worker.process
        )

        args = {
            "pipeline_name": pipeline.name,
            "from_state": pipeline_worker.from_state,
            "to_states": list(pipeline_worker.to_states),
            "limit": pipeline_worker.limit,
            "sort": pipeline_worker.sort,
        }

        desired_worker_ids.add(worker_id)
        if worker_id not in actual_workers:
            logger.info(f"Adding pipeline worker {worker_id}")
            worker_config_store.add(
                WorkerMetadata(
                    module_name=worker_id,
                    args=args,
                    interval_seconds=60,
                    error_resiliency=-1,
                )
            )
        else:
            logger.info(f"Updating pipeline worker {worker_id}")
            worker_config_store.update_args(worker_id, args)

    for worker_id in actual_workers.keys() - desired_worker_ids:
        logger.info(f"Removing pipeline worker {worker_id}")
        worker_config_store.remove(worker_id)

    # Remove workers if the pipeline is renamed or removed
    # DO NOT CHANGE this namespace, otherwise reconciliation won't find existing workers
    actual_all_pipeline_workers = worker_config_store.get_all(
        namespace="pipeline"
    )
    for worker_id in actual_all_pipeline_workers.keys() - desired_worker_ids:
        logger.info(f"Removing pipeline worker {worker_id} ({pipeline.name} gone)")
        worker_config_store.remove(worker_id)


def configure_pipeline_mod_views(
        pipeline: Pipeline,
        mod_view_store: ModViewStore,
):
    logger.info("Configuring pipeline mod views")

    def generate_mod_view_projections(
            to_state: PipelineModViewToState,
    ) -> NamedModViewColumn:
        update_set_doc = to_state.update_set_doc if to_state.update_set_doc else {}
        new_update_set_doc = copy.deepcopy(update_set_doc)
        new_update_set_doc[StateKey] = to_state.to_state

        return NamedModViewColumn(
            name=to_state.name,
            column=UpdateOneButton(
                text=to_state.name,
                filter_q_key=mod_view.filter_q_key,
                update_set_doc=new_update_set_doc,
                after_callback=ButtonAfterCallbackBehavior.RemoveRow,
            ),
        )

    # Add mod views
    for mod_view in pipeline.mod_views:
        mod_view_store.add_mod_view(
            name=mod_view.name,
            mod_view=ModViewQuery(
                query={StateKey: mod_view.from_state},
                projections=mod_view.projections
                            + list(map(generate_mod_view_projections, mod_view.to_states)),
                sort=mod_view.sort,
            ),
        )
