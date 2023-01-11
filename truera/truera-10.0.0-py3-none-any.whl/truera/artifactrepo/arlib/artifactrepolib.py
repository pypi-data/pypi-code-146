from enum import Enum
import hashlib
import itertools
import logging
import os
import shutil
from typing import Iterator, List

from filelock import FileLock

from truera.client.errors import NotFoundError
from truera.client.errors import SimpleException
from truera.client.errors import TruException
from truera.protobuf.public import artifactrepo_pb2 as ar_pb
from truera.protobuf.public.model_output_type_pb2 import \
    ModelOutputType  # pylint: disable=no-name-in-module
from truera.public.artifact_repo_lib import allowed_characters_description
from truera.public.artifact_repo_lib import valid_name_chars
from truera.utils.truera_status import TruEraAlreadyExistsError


# keep in sync with proto options
class ExistsOption(Enum):
    invalid = 0
    does_not_exist = 1
    file_exists = 2
    directory_exists = 3


class IllegalPathError(TruException):
    pass


class InvalidMapOptionError(TruException):
    pass


class EmptyIteratorError(SimpleException):
    pass


class ChecksumMismatchError(TruException):
    pass


class ArtifactRepositoryImpl(object):

    def __init__(self, repo_path: str):
        self.repoHome = os.path.join(repo_path)
        self.logger = logging.getLogger(__name__)

    def put_artifact(
        self, put_itr, logger, onfirst_callback: callable, audit_event: dict
    ):
        itr_for_locking, itr_for_ingest = itertools.tee(put_itr, 2)
        first_project_id, first_artifact_type, first_artifact_id, _, _, first_scoping_ids, _ = next(
            itr_for_locking
        )
        audit_event["project_id"], audit_event["artifact_id"], audit_event[
            "request_type"
        ] = first_project_id, first_artifact_id, first_artifact_type
        if onfirst_callback:
            # this callback will check whether the current user
            # has permission to upload to this project.
            onfirst_callback(first_project_id, first_artifact_id)

        artifact_path = self._get_project_id_path(
            first_project_id, first_artifact_type, first_artifact_id,
            first_scoping_ids
        )
        os.makedirs(os.path.dirname(artifact_path), exist_ok=True)
        artifact_lock_path = self._get_lock_path(artifact_path)
        # seems to be some disagreement about if FileLock vs pylint is at fault here, but no
        # evidence of a real issue: https://github.com/tox-dev/py-filelock/issues/102
        # We can loop back in AB#6110.
        # pylint: disable=abstract-class-instantiated
        lock = FileLock(artifact_lock_path, timeout=5)

        with lock:
            if os.path.isfile(self._get_success_path(artifact_path)):
                raise TruEraAlreadyExistsError(
                    "Artifact already exists and cannot be overwritten: " +
                    artifact_path
                )
            elif os.path.isdir(artifact_path):
                self.delete_artifact(
                    first_project_id,
                    first_artifact_type,
                    first_artifact_id,
                    "",
                    first_scoping_ids,
                    logger,
                    lock=lock
                )

            for project_id, artifact_type, artifact_id, intra_artifact_path, input_chunk, scoping_ids, checksum in itr_for_ingest:
                # impl note: the following ensures that the user uploads only one kind of entity at
                # in a series of PUT requests. Hence we require the IDs and TYPEs of all the chunks to be
                # the same. Should this change in the future, and we permit a single sequence of PUTs
                # to upload to multiple projects, then we must also check for authorization for each
                # of those projects as we do for the first one above.
                assert project_id == first_project_id
                assert artifact_type == first_artifact_type
                assert artifact_id == first_artifact_id
                # pylint: disable=no-member
                assert checksum is None or checksum.type == ar_pb.ResourceChecksum.ChecksumType.MD5
                if checksum:
                    computed_checksum = hashlib.md5( # nosec B324 - not using for security
                        input_chunk
                    ).hexdigest()
                    if computed_checksum != checksum.value:
                        raise ChecksumMismatchError(
                            f"Checksum mismatch for project: {project_id}, artifact: {artifact_id}, "
                            f" path: {intra_artifact_path}. Expected: {checksum.value}, Found: {computed_checksum}"
                        )
                destination_intra_project_path = self._get_ar_repo_path(
                    project_id, artifact_type, artifact_id, intra_artifact_path,
                    first_scoping_ids
                )
                self._append(destination_intra_project_path, input_chunk)
                logger.info(
                    ("Put chunk to {} in project {}."
                    ).format(destination_intra_project_path, project_id)
                )

            with open(self._get_success_path(artifact_path), "w") as f:
                pass

        return artifact_path

    def artifact_exists(
        self, project_id: str, artifact_type: str, artifact_id,
        intra_artifact_path: str, scoping_artifact_ids: List[str], logger
    ) -> ExistsOption:
        repo_path = self._get_ar_repo_path(
            project_id, artifact_type, artifact_id, intra_artifact_path,
            scoping_artifact_ids
        )

        # if the .success file is not there, we don't want to show the artifact as created
        artifact_path = self._get_project_id_path(
            project_id, artifact_type, artifact_id, scoping_artifact_ids
        )
        if not os.path.isfile(self._get_success_path(artifact_path)):
            logger.info(
                "Exist request for " + repo_path +
                " found artifact does not exist."
            )
            return ExistsOption.does_not_exist

        if os.path.isdir(repo_path):
            logger.info(
                "Exist request for " + repo_path + " found directory exists."
            )
            return ExistsOption.directory_exists
        elif os.path.isfile(repo_path):
            logger.info(
                "Exist request for " + repo_path + " found file exists."
            )
            return ExistsOption.file_exists
        else:
            logger.info(
                "Exist request for " + repo_path +
                " found artifact does not exist."
            )
            return ExistsOption.does_not_exist

    def get_artifact(
        self, project_id: str, artifact_type: str, artifact_id: str,
        intra_artifact_path: str, max_chunk_size: int,
        scoping_artifact_ids: List[str], logger
    ):
        artifact_path = self._get_project_id_path(
            project_id, artifact_type, artifact_id, scoping_artifact_ids
        )
        if not os.path.isfile(self._get_success_path(artifact_path)):
            message = "Artifact at  " + artifact_path + " does not exist."
            logger.warning(message)
            raise NotFoundError(message)

        repo_path = self._get_ar_repo_path(
            project_id, artifact_type, artifact_id, intra_artifact_path,
            scoping_artifact_ids
        )

        for relative_output_file_path, full_output_file_path in flatten(
            repo_path, logger
        ):
            for output_chunk in self._get(
                full_output_file_path, max_chunk_size
            ):
                logger.info(("Got chunk from artifact {}.").format(repo_path))
                yield output_chunk, relative_output_file_path

    def delete_artifact(
        self,
        project_id: str,
        artifact_type: str,
        artifact_id: str,
        intra_artifact_path: str,
        scoping_artifact_ids: List[str],
        logger,
        *,
        lock=None
    ):
        artifact_path = self._get_project_id_path(
            project_id, artifact_type, artifact_id, scoping_artifact_ids
        )
        artifact_lock_path = self._get_lock_path(artifact_path)
        friendly_name = os.path.join(
            artifact_type, artifact_id, intra_artifact_path
        )

        if not os.path.isdir(os.path.dirname(artifact_path)):
            message = "Path " + friendly_name + " does not exist in project " + project_id
            logger.info(message)
            raise NotFoundError(message)

        # seems to be some disagreement about if FileLock vs pylint is at fault here, but no
        # evidence of a real issue: https://github.com/tox-dev/py-filelock/issues/102
        # We can loop back in AB#6110.
        # pylint: disable=abstract-class-instantiated
        lock = lock or FileLock(artifact_lock_path, timeout=5)

        with lock:
            repo_path = self._get_ar_repo_path(
                project_id, artifact_type, artifact_id, intra_artifact_path,
                scoping_artifact_ids
            )
            if os.path.isdir(repo_path):
                contents = [
                    full_path for _, full_path in flatten(repo_path, logger)
                ]
                logger.info(f"Directory contents: {contents}")
                shutil.rmtree(repo_path)
                message = "Removed directory " + friendly_name
                if os.path.isfile(self._get_success_path(artifact_path)):
                    os.unlink(self._get_success_path(artifact_path))
                logger.info(message)
            elif os.path.isfile(repo_path):
                os.unlink(repo_path)
                message = "Removed file " + friendly_name
                if os.path.isfile(self._get_success_path(artifact_path)):
                    os.unlink(self._get_success_path(artifact_path))
                logger.info(message)
            else:
                message = "Path " + friendly_name + " does not exist in project " + project_id
                logger.info(message)
                raise NotFoundError(message)

        # If we're removing the whole artifact then also clean up the lock file
        if not intra_artifact_path:
            os.unlink(self._get_lock_path(artifact_path))

    # Prevent any piece from performing non-trivial combining operations. The
    # most problematic one would be '/' because os.path.join will restart if
    # it encounters an absolute path.
    def _assert_simple_directory_name(self, toCheck, *, extra_allowed_chars=[]):
        for piece in toCheck:
            for letter in piece:
                if (not letter in valid_name_chars
                   ) and (not letter in extra_allowed_chars):
                    extra_allowed_chars_dbg_string = self._get_str_for_extra_allowed_chars(
                        extra_allowed_chars
                    )

                    raise IllegalPathError(
                        "Illegal character: '" + letter + "'" + " in: " +
                        piece + ". Allowed characters: " +
                        allowed_characters_description +
                        extra_allowed_chars_dbg_string
                    )

    def _get_str_for_extra_allowed_chars(self, extra_allowed_chars):
        extra_allowed_chars_str = ""
        for extra in extra_allowed_chars:
            extra_allowed_chars_str = extra_allowed_chars_str + extra + ", "

        if extra_allowed_chars_str.endswith(', '):
            extra_allowed_chars_str = extra_allowed_chars_str[:-2]

        if len(extra_allowed_chars_str) > 0:
            extra_allowed_chars_str = ", " + extra_allowed_chars_str

        return extra_allowed_chars_str

    def _assert_not_starts_with(self, toCheck, not_allowed):
        for char in not_allowed:
            if toCheck.startswith(char):
                raise IllegalPathError(
                    "Intra artifact path starts with: '" + char +
                    "'. Absolute paths are not allowed. Intra artifact path: " +
                    toCheck + ". Allowed characters: " +
                    allowed_characters_description
                )

    def _get_ar_repo_path(
        self, project: str, artifact_type: str, artifact_id: str,
        intra_artifact_path: str, scope_ids: List[str]
    ):
        # Don't allow any user provided pieces to combine in non trivial ways
        # in os.path.join. This is meant to prevent file system changes outside
        # the artifact repo.
        self._assert_simple_directory_name(
            [project, artifact_type, artifact_id, *scope_ids]
        )
        # Since the intra_artifact_path may contain / we can only check that it
        # doesn't start with / to disallow passing /home/...
        self._assert_not_starts_with(intra_artifact_path, ['/', '.'])
        self._assert_simple_directory_name(
            [intra_artifact_path], extra_allowed_chars=['/', '.']
        )

        # Note that os.path.join will start combining over if it encounters an
        # absolute path.
        return os.path.join(
            self.repoHome, project, artifact_type, *scope_ids, artifact_id,
            intra_artifact_path
        )

    def _get_project_id_path(
        self, project_id: str, artifact_type: str, artifact_id: str,
        scope_ids: List[str]
    ):
        self.logger.info(
            f"{project_id} {artifact_type} {artifact_id} {scope_ids}"
        )
        self._assert_simple_directory_name(
            [project_id, artifact_type, artifact_id, *scope_ids]
        )

        # Note that os.path.join will start combining over if it encounters an
        # absolute path.
        return os.path.join(
            self.repoHome, project_id, artifact_type, *scope_ids, artifact_id
        )

    def _get_lock_path(self, path: str):
        return path + ".lock"

    def _get_success_path(self, path: str):
        return path + ".success"

    def _append(self, dest: str, chunk: bytes):
        os.makedirs(os.path.dirname(dest), exist_ok=True)

        with open(dest, "ab") as f:
            f.write(chunk)
        return dest

    def _get(self, repo_path: str, max_size: int) -> Iterator[str]:
        with open(repo_path, "rb") as f:
            while True:
                contents = f.read(max_size)
                if not contents:
                    break
                yield contents


def flatten(path: str, logger):
    """[summary]
    flattens a file or directory into:
        for a directory:
            for every file under the directory recursively:
                the relative path to the file relative to the input dir, full path to file in the repo
        for a file:
            the file name, the full path to the file in the repo

    Arguments:
        path {str} -- [description]

    Raises:
        ValueError: [description]

    Yields:
        [type] -- [description]
    """
    if os.path.isdir(path):
        for (dir_path, _, file_names) in os.walk(path):
            for file_name in file_names:
                joined_path = os.path.join(dir_path, file_name)

                if file_name == ".DS_Store":
                    continue

                if ".ipynb_checkpoints" in joined_path:
                    continue

                yield os.path.relpath(joined_path, path), joined_path
    elif os.path.isfile(path):
        _, filename = os.path.split(path)
        yield filename, path
    else:
        message = "Path is invalid:" + path
        if logger is not None:
            logger.error(message)
        raise NotFoundError(message)


def map_model_output_type(model_output_type):
    # If we already had the protobuf type, just return.
    # This allows some callers to not have to map into a string for us to map back.
    if type(model_output_type) == type(ModelOutputType.UNKNOWN_MODELOUTPUTTYPE):
        return model_output_type

    if model_output_type.lower() == "classification":
        return ModelOutputType.CLASSIFICATION
    if model_output_type.lower() == "regression":
        return ModelOutputType.REGRESSION
    if model_output_type.lower() == "default":
        return ModelOutputType.UNKNOWN_MODELOUTPUTTYPE
    else:
        raise InvalidMapOptionError(
            "The provided type {} was not valid.".format(model_output_type)
        )


def safe_dict_access(d, keys):
    for k in keys:
        if not isinstance(d, dict):
            return None
        if k not in d.keys():
            return None
        d = d[k]
    return d
