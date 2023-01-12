import argparse
import importlib
import logging


def cli():
    parser = argparse.ArgumentParser()
    parser.add_argument("--path", type=str, default=".")
    parser.add_argument("--log-level", type=logging_level, default="INFO")
    parser.add_argument(
        "--lock-class", type=class_import, default="fs_task_queue.core.DummyLock"
    )
    parser.add_argument(
        "--job-serializer-class",
        type=class_import,
        default="fs_task_queue.core.JSONSerializer",
    )
    parser.add_argument(
        "--result-serializer-class",
        type=class_import,
        default="fs_task_queue.core.JSONSerializer",
    )
    parser.add_argument(
        "--queue-class", type=class_import, default="fs_task_queue.core.Queue"
    )
    parser.add_argument(
        "--job-class", type=class_import, default="fs_task_queue.core.Job"
    )
    parser.add_argument(
        "--worker-class", type=class_import, default="fs_task_queue.core.Worker"
    )
    args = parser.parse_args()
    return handle_cli(args)


def logging_level(value):
    return getattr(logging, value)


def class_import(value):
    module, function = value.rsplit(".", 1)
    return getattr(importlib.import_module(module), function)


def handle_cli(args):
    logging.basicConfig(level=args.log_level)

    queue = args.queue_class(
        directory=args.path,
        job_serializer_class=args.job_serializer_class,
        result_serializer_class=args.result_serializer_class,
        lock_class=args.lock_class,
        job_class=args.job_class,
    )
    worker = args.worker_class(
        queue=queue,
    )
    worker.run()
