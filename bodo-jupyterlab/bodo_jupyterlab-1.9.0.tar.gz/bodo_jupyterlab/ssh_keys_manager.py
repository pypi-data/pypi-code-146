import glob
import os

from cachetools import TTLCache, cached
from cachetools.keys import hashkey

from .config import (
    SSH_KEY_DIR,
    GET_SSH_KEY_SCRIPT,
    SSH_KEY_FILE_PREFIX,
    GET_SSH_KEY_TIMEOUT_SECONDS,
    SSH_KEYS_CLEANUP_PERIOD_SECONDS,
)
from .helpers import execute_shell


def get_cluster_ssh_key_fname(cluster_uuid, logger, hard_refresh=False):
    logging_prefix = f"[GetClusterSSHKey][UUID: {cluster_uuid}]"
    fname = os.path.join(SSH_KEY_DIR, f"{SSH_KEY_FILE_PREFIX}{cluster_uuid}")
    logger.info(f"{logging_prefix} Expected Filename: {fname}")
    # If the file already exists, and we don't want to do a hard refresh,
    # then return this
    if os.path.exists(fname) and not hard_refresh:
        logger.info(f"{logging_prefix} {fname} exists. Returning...")
        return fname

    if not os.path.exists(GET_SSH_KEY_SCRIPT):
        logger.warning(f"{logging_prefix} {GET_SSH_KEY_SCRIPT} doesn't exist...")
        raise Exception(
            f"Could not locate script {GET_SSH_KEY_SCRIPT} to get the SSH key."
        )

    # Create the SSH keys directory if it doesn't already exist
    os.makedirs(SSH_KEY_DIR, exist_ok=True)
    stdout_, stderr_, returncode, timed_out = execute_shell(
        f"sh {GET_SSH_KEY_SCRIPT} {cluster_uuid} {fname}",
        timeout=GET_SSH_KEY_TIMEOUT_SECONDS,
    )
    logger.debug(f"{logging_prefix} Script Exec returncode: {returncode}")
    logger.debug(f"{logging_prefix} Script Exec timed_out: {timed_out}")
    logger.debug(f"{logging_prefix} Script Exec STDOUT:\n{stdout_}")
    logger.debug(f"{logging_prefix} Script Exec STDERR:\n{stderr_}")
    if returncode == 0 and os.path.exists(fname):
        logger.info(f"{logging_prefix}: SUCCESS")
        return fname
    else:
        logger.warning(f"{logging_prefix}: FAILED")
        if returncode != 0:
            e = f"There was an error while executing {GET_SSH_KEY_SCRIPT}. See logs."
            logger.warning(f"{logging_prefix}: {e}")
            raise Exception(e)
        else:
            # File doesn't exist
            e = f"{GET_SSH_KEY_SCRIPT} was executed successfully but file wasn't found subsequently (expected at {fname})."
            logger.warning(f"{logging_prefix}: {e}")
            raise Exception(e)


# Can only be called once every SSH_KEYS_CLEANUP_PERIOD_SECONDS seconds
@cached(
    cache=TTLCache(maxsize=2, ttl=SSH_KEYS_CLEANUP_PERIOD_SECONDS),
    key=lambda logger, active_cluster_uuids: hashkey("A"),
)
def cleanup_ssh_keys(logger, active_cluster_uuids):
    """
    Clean up SSH keys from jupyter instance
    :param logger: Logger object
    :param active_cluster_uuids: Set of all cluster uuids that are not in FAILED/TERMINATED state
    """
    logging_prefix = "[SSHKeys Cleanup]"
    logger.info(f"{logging_prefix} Starting...")
    logger.info(f"{logging_prefix} cluster_uuids: {active_cluster_uuids}")

    existing_ssh_key_files = glob.glob(
        os.path.join(SSH_KEY_DIR, f"{SSH_KEY_FILE_PREFIX}*")
    )
    # Convert to a dict (cluster_uuid -> filename)
    existing_ssh_key_files = {
        os.path.basename(x)[len(SSH_KEY_FILE_PREFIX) :]: x
        for x in existing_ssh_key_files
    }

    logger.info(f"{logging_prefix} existing_ssh_key_files: {existing_ssh_key_files}")

    # If the SSH key is for a cluster that is no longer active,
    # then remove it
    for cluster_uuid, fname in existing_ssh_key_files.items():
        if cluster_uuid not in active_cluster_uuids:
            logger.info(f"{logging_prefix} Deleting SSH Key {fname}")
            os.remove(fname)
