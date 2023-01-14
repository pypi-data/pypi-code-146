from typing import Optional
from flask import Blueprint, jsonify
from katatachi.worker import WorkerConfigStore, WorkerCache
from katatachi.content import ContentStore
from katatachi.pipeline.pipeline import Pipeline


def pipeline_blueprint_factory(
        pipeline: Optional[Pipeline],
        worker_config_store: WorkerConfigStore,
        worker_cache: WorkerCache,
        content_store: ContentStore,
):
    blueprint = Blueprint('pipeline', __name__)

    @blueprint.route('', methods=['GET'])
    def _get():
        if not pipeline:
            return None, 404

        source_workers = []
        for worker_id, worker in worker_config_store.get_all().items():
            if worker_cache.is_module_pipeline_source(worker.module_name):
                source_workers.append(worker_id)

        return (
            jsonify(
                {
                    "pipeline": pipeline.to_dict(content_store),
                    "sources": source_workers,
                }
            ),
            200,
        )

    return blueprint
