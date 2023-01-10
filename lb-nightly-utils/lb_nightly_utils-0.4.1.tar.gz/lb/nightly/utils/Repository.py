###############################################################################
# (c) Copyright 2020-2021 CERN for the benefit of the LHCb Collaboration      #
#                                                                             #
# This software is distributed under the terms of the GNU General Public      #
# Licence version 3 (GPL Version 3), copied verbatim in the file "LICENSE".   #
#                                                                             #
# In applying this licence, CERN does not waive the privileges and immunities #
# granted to it by virtue of its status as an Intergovernmental Organization  #
# or submit itself to any jurisdiction.                                       #
###############################################################################
"""
Code handling interactions with artifacts repository
"""

import logging
import os
from contextlib import contextmanager
from http import HTTPStatus
from io import BytesIO
from os import makedirs
from os.path import dirname, exists, join
from shutil import copyfileobj
from subprocess import CalledProcessError, run
from tempfile import NamedTemporaryFile, mkstemp
from time import sleep

import boto3
import lb.nightly.configuration
from botocore.exceptions import ClientError
from requests import get, head, put
from requests.compat import urljoin, urlparse, urlunparse

_repo_handlers = {}


def register_for(*schemes):
    """
    Decorator used to register the concrete type of repository
    """

    def _reg(cls):
        global _repo_handlers
        _repo_handlers.update((s, cls) for s in schemes)
        return cls

    return _reg


def get_repo_type(uri):
    """
    Returns type of repository based on uri provided in the argument.
    It may return "eos", "file", "http" or None
    """

    result = urlparse(uri)
    if not result.scheme or result.scheme == "file":
        return "file"
    elif result.scheme == "root":
        return "eos"
    elif result.scheme in ("http", "https"):
        return "http"
    elif result.scheme in ("s3", "s3+https"):
        return "s3"
    return None


class ArtifactsRepository(object):
    """
    Class representing artifacts repository.
    """

    def __init__(self, uri):
        """
        Initialises the repository based on its URI
        """
        self.uri = uri

    def pull(self, artifacts_name):
        """
        Pulls artifact from repository as in-memory binary stream.
        Raises exceptions if the artifact cannot be opened.

        Arguments:
        artifacts_name: name of the artifacts file

        Returns: BytesIO object
        """
        raise NotImplementedError("Should be implemented in the inheriting class")

    def push(self, file_object, remote_name):
        """
        Pushes artifacts to the repository

        Arguments:
        file_object: file object with the data to be pushed to repository
        remote_name: name of the artifcats file in the repository

        Returns: True if the artifacts have been pushed, False otherwise
        """
        raise NotImplementedError("Should be implemented in the inheriting class")

    def exist(self, artifacts_name):
        """
        Checks if artifacts exist

        Arguments:
        artifacts_name: name of the artifcats file

        Returns: True if the artifacts exist, False otherwise
        """
        raise NotImplementedError("Should be implemented in the inheriting class")

    def get_url(self, artifacts_name, **kwargs):
        """
        Get the URL to artifact

        Arguments: artifacts_name: name of the artifcats file
        Returns: URL as string
        """
        raise NotImplementedError("Should be implemented in the inheriting class")


@register_for(None)
def unknown_uri(uri):
    raise ValueError("Unsupported uri {!r}".format(uri))


@register_for("file")
class FileRepository(ArtifactsRepository):
    """
    Class defining repository in the local file system.
    """

    def __init__(self, uri):
        ArtifactsRepository.__init__(self, uri)
        self.root = os.path.join(os.getcwd(), urlparse(self.uri).path)

    def pull(self, artifacts_name):
        with open(join(self.root, artifacts_name), "rb") as f:
            artifact = f.read()
        return BytesIO(artifact)

    def push(self, file_object, remote_name):
        try:
            makedirs(join(self.root, dirname(remote_name)))
        except OSError:
            pass
        fdst = open(join(self.root, remote_name), "wb")
        try:
            copyfileobj(file_object, fdst)
        except IOError:
            return False
        return True

    def exist(self, artifacts_name):
        return exists(join(self.root, artifacts_name))


@register_for("eos")
class EosRepository(ArtifactsRepository):
    """
    Class defining repository on EOS.
    """

    def __init__(self, uri, **kwargs):
        ArtifactsRepository.__init__(self, uri)
        urlparts = urlparse(self.uri)
        self.host = urlunparse((urlparts.scheme, urlparts.netloc, "", "", "", ""))
        self.root = urlparts.path.replace("//", "/")
        try:
            user = kwargs["user"]
        except KeyError:
            raise KeyError("missing user in the artifacts repository configuration")
        keytab = kwargs.get("keytab", "")
        password = kwargs.get("password", "")
        assert keytab or password, "missing keytab or password"
        self._krb_token = NamedTemporaryFile()
        if keytab:
            run(
                ["kinit", "-c", self._krb_token.name, "-k", "-t", keytab, user],
                check=True,
            )
        elif password:
            run(
                ["kinit", "-c", self._krb_token.name, user],
                input=password.encode(),
                check=True,
            )

    @contextmanager
    def _authenticated_env(self):
        env = dict(os.environ)
        env["KRB5CCNAME"] = f"FILE:{self._krb_token.name}"
        yield env

    def pull(self, artifacts_name):
        fd, path = mkstemp()
        with self._authenticated_env() as env:
            run(
                ["xrdcp", "-f", join(self.uri, artifacts_name), path],
                check=True,
                env=env,
            )
        with open(path, "rb") as f:
            artifact = f.read()
        os.close(fd)
        os.remove(path)
        return BytesIO(artifact)

    def push(self, file_object, remote_name):
        with self._authenticated_env() as env:
            run(
                [
                    "xrdfs",
                    self.host,
                    "mkdir",
                    "-p",
                    join(self.root, dirname(remote_name)),
                ],
                check=True,
                env=env,
            )
        fd, path = mkstemp()
        with open(path, "wb") as f:
            f.write(file_object.read())
        try:
            with self._authenticated_env() as env:
                run(
                    ["xrdcp", "-f", path, join(self.uri, remote_name)],
                    check=True,
                    env=env,
                )
        except CalledProcessError as ex:
            logging.warning(f"Pushing artifacts to the repository failed: {ex}")
            return False
        finally:
            os.close(fd)
            os.remove(path)
        return True

    def exist(self, artifacts_name):
        try:
            with self._authenticated_env() as env:
                run(
                    ["xrdfs", self.host, "stat", join(self.root, artifacts_name)],
                    check=True,
                    env=env,
                )
        except CalledProcessError:
            return False
        return True


@register_for("http")
class HttpRepository(ArtifactsRepository):
    """
    Class defining repository through HTTP request methods.
    """

    def __init__(self, uri, **kwargs):
        # extract authentication details from the URL, if present
        parts = urlparse(uri)
        netloc = parts.netloc
        user = password = None
        if "@" in netloc:
            user, netloc = netloc.split("@", 1)
            if ":" in user:
                user, password = user.split(":", 1)
            # rebuild the uri without the authetication details
            uri = urlunparse(
                (
                    parts.scheme,
                    netloc,
                    parts.path,
                    parts.params,
                    parts.query,
                    parts.fragment,
                )
            )

        ArtifactsRepository.__init__(self, uri)

        # copy user and password to the arguments, if needed
        if "user" not in kwargs and user:
            kwargs["user"] = user
        if "password" not in kwargs and password:
            kwargs["password"] = password

        try:
            self.auth = kwargs["user"], kwargs["password"]
        except KeyError as ke:
            raise KeyError(f"missing {ke} in the artifacts repository configuration")

    def pull(self, artifacts_name):
        r = get(urljoin(self.uri, artifacts_name))
        r.raise_for_status()
        return BytesIO(r.content)

    def push(self, file_object, remote_name):
        # allow for a few attempts with increasing delay to account
        # for temporary unavailabilities of the service
        for wait in [0, 1, 2, 4, 8, 16, 32, 64, 128, 256]:
            sleep(wait)
            logging.debug(f"Pushing to {remote_name}")
            file_object.seek(0)
            r = put(
                urljoin(self.uri, remote_name),
                data=file_object,
                auth=self.auth,
            )
            if r.status_code == HTTPStatus.CREATED:
                logging.debug(f"Successfully pushed to {remote_name}")
                return True
            else:
                logging.debug(f"Failed to push: status == {r.status_code}")
        logging.error(f"Failed to push: status == {r.status_code}")
        logging.error(f"Server response: {r.text}")
        return False

    def exist(self, artifacts_name):
        r = head(urljoin(self.uri, artifacts_name))
        if r.status_code == HTTPStatus.OK:
            return True
        return False

    def get_url(self, artifacts_name):
        """
        Get a URL to artifact
        Parameters:
          artifacts_name:
        Returns: URL as string.
        """
        return f"{self.uri}/{artifacts_name}"


@register_for("s3")
class S3Repository(ArtifactsRepository):
    """
    Class defining S3 repository.
    """

    def __init__(self, uri, **kwargs):
        try:
            # if the uri scheme has the form of s3+https, we need to drop the s3 part
            uri = uri.split("+")[1]
        except IndexError:
            pass
        try:
            self.client = boto3.client(
                "s3",
                endpoint_url=uri,
                region_name=kwargs["region_name"],
                aws_access_key_id=kwargs["access_key_id"],
                aws_secret_access_key=kwargs["secret_access_key"],
            )
            self.bucket = kwargs["bucket"]
        except KeyError as ke:
            raise KeyError(f"missing {ke} in the artifacts repository configuration")
        try:
            self.client.head_bucket(Bucket=self.bucket)
        except ClientError as e:
            self.client.create_bucket(Bucket=self.bucket)

        ArtifactsRepository.__init__(self, uri)

    def pull(self, artifacts_name):
        with NamedTemporaryFile() as data:
            self.client.download_fileobj(self.bucket, artifacts_name, data)
            data.seek(0)
            out = data.read()
        return BytesIO(out)

    def push(self, file_object, remote_name):
        self.client.upload_fileobj(file_object, self.bucket, remote_name)
        return self.exist(remote_name)

    def exist(self, artifacts_name):
        try:
            self.client.head_object(Bucket=self.bucket, Key=artifacts_name)
        except ClientError as e:
            return int(e.response["Error"]["Code"]) != 404
        return True

    def get_url(self, artifacts_name):
        """
        Get a URL to artifact
        Parameters:
          artifacts_name:
        Returns: URL as string.
        """
        return f"{self.uri}/{self.bucket}/{artifacts_name}"


def connect(uri=None, *args, **kwargs):
    """
    Function returning the artifacts repository object based
    on the URI defined in lb.nightly.configuration.service_config()
    or provided in the argument.
    """
    global _repo_handlers
    try:
        config = (lb.nightly.configuration.service_config() or {}).get("artifacts", {})
    except FileNotFoundError:
        config = {}
    if uri is None:
        try:
            uri = config["uri"]
        except KeyError:
            raise KeyError("missing URI of the artifacts repository")
    return _repo_handlers[get_repo_type(uri)](
        uri, *args, **{**kwargs, **{k: v for k, v in config.items() if k != "uri"}}
    )
