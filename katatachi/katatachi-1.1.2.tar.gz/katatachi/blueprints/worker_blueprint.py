from flask import jsonify
from flask import request
from flask import Blueprint
from katatachi.worker.global_metadata_store import GlobalMetadataStore
from katatachi.worker.worker_cache import WorkerCache
from katatachi.worker.worker_config_store import WorkerConfigStore
from katatachi.worker.worker_metadata import WorkerMetadata
from katatachi.worker.worker_run_store import WorkerRunStore


def worker_blueprint_factory(
        worker_cache: WorkerCache,
        worker_config_store: WorkerConfigStore,
        global_metadata_store: GlobalMetadataStore,
        worker_run_store: WorkerRunStore
):
    blueprint = Blueprint('worker', __name__)

    @blueprint.route("modules", methods=["GET"])
    def _get_worker_modules():
        return (
            jsonify(
                list(map(lambda m: m.to_json(), worker_cache.get_modules()))
            ),
            200,
        )

    @blueprint.route("", methods=["POST"])
    def _add_worker():
        payload = request.json
        status, message_or_worker_id = worker_config_store.add(
            WorkerMetadata(
                module_name=payload["module_name"],
                args=payload["args"],
                interval_seconds=payload["interval_seconds"],
                error_resiliency=-1,
            )
        )
        if not status:
            return (
                jsonify({"status": "error", "message": message_or_worker_id}),
                400,
            )
        else:
            return jsonify({"status": "ok", "worker_id": message_or_worker_id}), 200

    @blueprint.route("", methods=["GET"])
    def _get_workers():
        workers = []
        for worker_id, worker in worker_config_store.get_all().items():
            workers.append(
                {
                    "worker_id": worker_id,
                    "module_name": worker.module_name,
                    "args": worker.args,
                    "interval_seconds": worker.interval_seconds,
                    "error_resiliency": worker.error_resiliency,
                    "last_executed_seconds": worker_config_store.get_last_executed_seconds(
                        worker_id
                    ),
                }
            )
        return jsonify(workers), 200

    @blueprint.route("<string:worker_id>", methods=["DELETE"])
    def _remove_worker(worker_id: str):
        status, message = worker_config_store.remove(worker_id)
        if not status:
            return jsonify({"status": "error", "message": message}), 400
        else:
            return jsonify({"status": "ok"}), 200

    @blueprint.route(
        "<string:worker_id>/intervalSeconds/<int:interval_seconds>",
        methods=["PUT"],
    )
    def _update_worker_interval_seconds(worker_id: str, interval_seconds: int):
        status, message = worker_config_store.update_interval_seconds(
            worker_id, interval_seconds
        )
        if not status:
            return jsonify({"status": "error", "message": message}), 400
        else:
            return jsonify({"status": "ok"}), 200

    @blueprint.route(
        "<string:worker_id>/errorResiliency/<signed_int:error_resiliency>",
        methods=["PUT"],
    )
    def _update_worker_error_resiliency(worker_id: str, error_resiliency: int):
        status, message = worker_config_store.update_error_resiliency(
            worker_id, error_resiliency
        )
        if not status:
            return jsonify({"status": "error", "message": message}), 400
        else:
            return jsonify({"status": "ok"}), 200

    @blueprint.route(
        "<string:worker_id>/metadata", methods=["GET"]
    )
    def _get_worker_metadata(worker_id: str):
        return jsonify(global_metadata_store.get_all(worker_id)), 200

    @blueprint.route(
        "<string:worker_id>/metadata", methods=["POST"]
    )
    def _set_worker_metadata(worker_id: str):
        parsed_body = request.json
        global_metadata_store.set_all(worker_id, parsed_body)
        return jsonify({"status": "ok"}), 200

    @blueprint.route("<string:worker_id>/args", methods=["GET"])
    def _get_worker_args(worker_id: str):
        return jsonify(worker_config_store.get_args(worker_id)), 200

    @blueprint.route("runs", methods=["GET"])
    def _get_worker_runs():
        page = request.args.get('page', default=1, type=int)
        return jsonify(worker_run_store.get_runs(page)), 200

    return blueprint
