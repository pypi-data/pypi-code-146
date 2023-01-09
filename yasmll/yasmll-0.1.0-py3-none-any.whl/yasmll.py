import jax
import tensorflow as tf


def init(coordinator_address="localhost:12340", num_processes=1, process_id=0, local_devices_ids=None):
    """Initializes JAX and other distributed services.

    Args:
        coordinator_address:
        num_processes:
        process_id:
        local_devices_ids:
    """
    # Turn all GPUs invisible to TensorFlow
    tf.config.set_visible_devices([], "GPU")

    # Initialize JAX distributed environment
    jax.distributed.initialize(
        coordinator_address=coordinator_address,
        num_processes=num_processes,
        process_id=process_id,
        local_device_ids=local_devices_ids,
    )


def shutdown():
    """Finalizes JAX and all other distributed tasks."""
    # Shutdown JAX distributed service.
    jax.distributed.shutdown()
