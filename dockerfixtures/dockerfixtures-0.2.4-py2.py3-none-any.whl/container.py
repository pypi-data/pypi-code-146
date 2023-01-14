# -*- coding: utf-8; -*-
"""Container classes and factory functions


"""
import logging
from socket import AF_INET, AF_INET6, SOCK_DGRAM, SOCK_STREAM, socket
from time import sleep, time
from typing import Any, Callable, cast, Dict, Generator, List, Mapping, Optional, Tuple, Union
import warnings

import docker
from docker.models import images
import requests.exceptions

from . import ci
from .image import Image


__all__ = ('ci_fixture', 'Container', 'fixture')

_CONTAINER_DEFAULT_OPTIONS = dict(cap_add=['IPC_LOCK'],
                                  # mem_limit='256m',
                                  # privileged=True,
                                  detach=True,
                                  publish_all_ports=True
                                  )

CONTAINER_STATUS_CREATED = 'created'
CONTAINER_STATUS_DEAD = 'dead'
CONTAINER_STATUS_EXITED = 'exited'
CONTAINER_STATUS_PAUSED = 'paused'
CONTAINER_STATUS_RUNNING = 'running'
# Couldn't find those in the docker module... need to look harder

_CONTAINER_STATUSES_KO = (CONTAINER_STATUS_DEAD,
                          CONTAINER_STATUS_EXITED,
                          )
_CONTAINER_STATUSES_OK = (CONTAINER_STATUS_RUNNING,
                          )
_CONTAINER_STATUSES_WAIT = (CONTAINER_STATUS_CREATED,
                            CONTAINER_STATUS_PAUSED,
                            )
_SUPPORTED_NETWORK_PROTOCOLS = ['tcp', 'udp']

MANIFEST_V2 = 'application/vnd.docker.distribution.manifest.v2+json'
MANIFEST_LIST_V2 = 'application/vnd.docker.distribution.manifest.list.v2+json'
SUPPORTED_MANIFEST_TYPES = (MANIFEST_V2, MANIFEST_LIST_V2)


class TimeOut(Exception):
    """Raised when a container does not start within the alloted time
    """


class ImageNotFound(Exception):
    """Raised when an image cannot be found in the docker registry
    """


class UnsupportedNetworkProtocol(Exception):
    """Raised when a port value contains an invalid protocol name
    """


def _port(port: str) -> Tuple[int, str]:
    """Transforms ports in the '<port>/<proto>' syntax into a tuple.
    """
    if '/' in port:
        port_, proto = port.split('/')  # type: Tuple[str, Optional[str]]
    else:
        port_, proto = port, None

    if not proto:
        return int(port_), 'tcp'
    if proto not in _SUPPORTED_NETWORK_PROTOCOLS:
        raise UnsupportedNetworkProtocol("Protocol '{}' is not supported, only {} are."
                                         .format(proto,
                                                 ' and '.join([
                                                     ', '.join(_SUPPORTED_NETWORK_PROTOCOLS[:-1]),
                                                     *_SUPPORTED_NETWORK_PROTOCOLS[:-1]])))
    return int(port_), proto


def _prune_dict(dictionary: Mapping[Any, Optional[Any]]) -> Mapping[Any, Any]:
    """Removes None values from pCallable, ossibly nested dict.

    Note: this function does not prune structures others than dict,
      for example print_dict({'k': [None, None]}) will not remove the
      None in the list.

    """
    res = {}
    for key, value in dictionary.items():
        if value is None:
            continue
        if isinstance(value, dict):
            value = _prune_dict(value)
            if len(value) > 0:
                res[key] = value
        else:
            res[key] = value
    return res


# class Service(Protocol):
#
#     @property
#     def address(self) -> str:
#         """The IP address of the created container.
#         """
#         ...
#
#     @property
#     def ports(self) -> Dict[str, Tuple[int, str]]:
#         """The ports the created container listens on.
#
#         """
#         ...


class Service:

    DEFAULT_MAX_WAIT = 1.0
    DEFAULT_READYNESS_POLL_INTERVAL = 10.0

    @property
    def address(self) -> str:
        """The IP address of the created container.
        """
        raise NotImplementedError()

    @property
    def max_wait(self) -> float:
        """The maximun amount of time to wait the container to be ready.
        """
        raise NotImplementedError()

    @property
    def ports(self) -> Dict[str, Tuple[int, str]]:
        """The ports the created container listens on.

        """
        raise NotImplementedError()

    @property
    def readyness_poll_interval(self) -> float:
        """The time interval at which check the container is ready.
        """
        raise NotImplementedError()


class WaiterMixin(Service):  # Inheritance not required with protocols
    """Mixin providing means to wait for a network port to be listening.

    The class this mixin blends with are expected to follow the Service
    protocol.
    """

    DEFAULT_MAX_WAIT = 1.0
    DEFAULT_READYNESS_POLL_INTERVAL = 10.0

    def wait(self: Service,
             *ports: Tuple[int, str],
             max_wait: float = 0.0,
             readyness_poll_interval: float = 0.1,
             ) -> bool:
        """Waits for the container to be listening on some network ports.
        """
        if not ports:
            next_round_ports = list(self.ports.values())
        else:
            next_round_ports = list(ports)
        max_wait = max_wait or self.max_wait or self.DEFAULT_MAX_WAIT
        readyness_poll_interval = (readyness_poll_interval or
                                   self.readyness_poll_interval
                                   or self.DEFAULT_READYNESS_POLL_INTERVAL)

        then = time()
        while (time() - then) < max_wait:
            ports_to_check = next_round_ports
            next_round_ports = []

            for port, proto in ports_to_check:
                try:
                    sock_proto = SOCK_STREAM if proto[:3] == 'tcp' else SOCK_DGRAM
                    with socket(AF_INET6 if proto[-1] == '6' else AF_INET, sock_proto) as sock:
                        sock.connect((self.address, port))
                except ConnectionError:
                    next_round_ports.append((port, proto))
                    sleep(readyness_poll_interval)

            if not next_round_ports:
                return True
        raise TimeOut('Container taking too long to become ready (waited {:.2f}s.): {} {}'
                      .format(time() - then,
                              self.address,
                              ', '.join(['{}/{}'.format(str(x[0]), x[1])
                                         for x in next_round_ports])))


class Container(WaiterMixin):  # , Service  # When 3.6 & 3.7 are dropped and we can use protocols
    """Represents a container
    """
    __slots__ = ('__client',
                 '__command',
                 '__container',
                 '__environment',
                 '__max_wait',
                 '__options',
                 '__readyness_poll_interval',
                 '__startup_poll_interval',
                 '_image',
                 )

    def __enter__(self):
        self.run()
        return self

    def __exit__(self, exc_type, exc_value, exc_tb):
        self.kill()
        self.remove()
        if exc_value:
            raise exc_value

    @staticmethod
    def __has_entrypoint(image):
        """Checks whether the docker image has an entrypoint defined
        """
        return ('Config' in image.attrs
                and 'Entrypoint' in image.attrs['Config']
                and image.attrs['Config']['Entrypoint'])

    def __init__(self,
                 image: Image,
                 *,
                 command: Optional[Union[str, List[str]]] = None,
                 dockerclient: docker.client.DockerClient = None,
                 environment: Mapping[str, str] = None,
                 max_wait: Optional[float] = None,
                 options: Optional[Mapping[str, Any]] = None,
                 startup_poll_interval: float = 1,
                 readyness_poll_interval: float = 0.2,
                 ):
        """

        TODO: Build container from an ID ? (restart paused container)
        """
        assert max_wait is None or max_wait > 0.0
        self.__client = dockerclient
        self.__command = command
        self.__container = None
        self.__environment = _prune_dict({** image.default_environment, **(environment or dict())})
        self._image = image
        self.__max_wait = max_wait or image.max_wait
        self.__options = options or dict()
        self.__readyness_poll_interval = readyness_poll_interval
        self.__startup_poll_interval = startup_poll_interval

    @property
    def address(self) -> str:
        """Returns the container's IP address
        """
        if self.__container is None:
            raise RuntimeError("Container not started, it can't have an address yet.")
        try:
            network = self.__container.attrs['NetworkSettings']
            ip = network['IPAddress']
        except KeyError:
            ip = ''

        if not ip:
            ip = 'localhost'  # !!
        return ip

    @property
    def id(self):
        """The identifier of the container, or None.

        The value None is only returnd if the container has not been
        started yet.

        """
        return self.__container.id if self.__container else None

    @property
    def image(self):
        """Returns the Image the container is based upon.
        """
        return self._image

    def kill(self):
        """Kills the container if still running.

        Equivalent to the `docker stop <ContainerID>` command
        """
        try:
            self.__container.kill()
        except requests.exceptions.HTTPError as exc:
            if exc.response.status_code != 409:
                raise
            # Container was already dead.

    @property
    def options(self) -> Dict[str, Any]:
        """Returns the options to use to create the container from the image.

        The value return by this attribute is the union of the default
        options (:var:`_CONTAINER_DEFAULT_OPTIONS`) and the optoins you
        passed upon the :class:`.Container` object construction.

        These are equivalent to the options you would pass to the
        :program:`docker` command line. The options in question exclude
        some that have dedicated arguments:

        - `environment` to manage the containers environment variables;
        - `environment` to manage the containers environment variables;

        """
        options = {**_CONTAINER_DEFAULT_OPTIONS, **self.__options}
        return options

    @property
    def max_wait(self) -> float:
        return self.__max_wait or self._image.max_wait

    @property
    def ports(self) -> Dict[str, Tuple[int, str]]:
        """Try to return the set of ports the container listens on.

        Return value is::

            {'<port>/proto': (<effective port>, 'proto'), }

        """
        # helps mypy understand the self.__client.images ... below
        # it can't guess that self.__container not None => self.__client not None.
        assert self.__client is not None

        if self.__container is not None:
            image = self.__container.image  # type: images.Image
        else:
            imagemeta: images.RegistryData = self.__client.images.get_registry_data(
                name=self._image.pullname)
            assert imagemeta.attrs['Descriptor']['mediaType'] in SUPPORTED_MANIFEST_TYPES
            image = cast(images.Image, imagemeta.pull())
        # Get list of exposed ports
        ports = {k: _port(k) for k, v in image.attrs.get('ExposedPorts', {}).items()}
        # Update with the possible port mapping(s)
        ports.update({k: _port(k) for k, v in self.__options.get('ports', {}).items()})
        return ports

    @property
    def readyness_poll_interval(self) -> float:
        return self.__readyness_poll_interval

    def remove(self) -> None:
        """Removes the container

        Equivalent to the `docker rm <ContainerID>` command
        """
        if self.__container is None:
            warnings.warn('Container was never started!', RuntimeWarning)
            return
        self.__container.remove(v=True, force=True)

    def run(self, command=None, dockerclient=None):
        """Starts the container

        Args:
            dockerclient: a docker client if none were provided on container instanciation
            command: alternate command for the container to run, instead its default CMD or
                ENTRYPOINT

        Raises:
            docker.errors.ImageNotFound: if the image to use to build the container cannot be found.
            docker.errors.APIError: if the docker server returns an Error, any other error.
            RuntimeError: if the container fails to start after
            ValueError: if you failed to

        """
        self.__client = dockerclient or self.__client  # Override client if requested
        if self.__client is None:
            raise ValueError('You did not provide a docker client !')

        try:
            image = self.__client.images.pull(self._image.pullname)
        except docker.errors.ImageNotFound as exc:
            raise ImageNotFound("Image '{}' does not exist".format(self._image.pullname)) from exc

        logging.getLogger(__name__).debug('Starting container from image: %s', self._image.name,
                                          extra={'pullname': self._image.pullname,
                                                 'environment': self.__environment,
                                                 'options': self.options,
                                                 })
        run_args = {'image': image,
                    'environment': self.__environment,
                    **self.options,
                    }
        if command or self.__command:
            override = 'command'
            if self.__has_entrypoint(image):
                override = 'entrypoint'
            run_args[override] = command or self.__command

        self.__container = self.__client.containers.run(**run_args)

        then = time()
        while (time() - then) < self.__max_wait:
            self.__container.reload()
            logging.getLogger(__name__).debug('Container %s status is %s',
                                              self.__container.id,
                                              self.__container.status)
            if self.__container.status in _CONTAINER_STATUSES_OK:  # pylint: disable=no-else-break
                break
            elif self.__container.status in _CONTAINER_STATUSES_KO:
                raise RuntimeError('Container stopped prematurely')
            elif self.__container.status not in _CONTAINER_STATUSES_WAIT:
                warnings.warn('Unknown container status!', RuntimeWarning)

            sleep(self.__startup_poll_interval)  # pylint: disable=expression-not-assigned
        else:
            raise TimeOut('Container {} is taking too long to start'
                          .format(self.__container.id))

        return self.__container.id


class FakeContainer(WaiterMixin):
    """A container that actually doesn't start a container

    This is intended for use in a context where Containers may be
    defined and started by means outside of your Python test suite.

    For example, more and more CI/CD are based on containers and
    starts them for you.

    This class is here to provide you with a drop-in replacement
    for the real :class:`.Container` class you don't need in such
    an environment, and present the same API, so you don't need to
    worry about who actually started the containers.

    """

    __slots__ = ('__address', '__ports')

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, exc_tb):
        if exc_value:
            raise exc_value

    def __init__(self, address, *ports, max_wait=None, readyness_poll_interval=None):
        self.__address = address
        self.__max_wait = max_wait
        self.__ports = ports
        self.__readyness_poll_interval = readyness_poll_interval

    @property
    def address(self) -> str:
        """The IP address of the created container.
        """
        return self.__address

    @property
    def max_wait(self) -> float:
        return self.__max_wait

    @property
    def ports(self) -> Dict[str, Tuple[int, str]]:
        """The ports the created container listens on.

        """
        return {f'{port}/{proto}': (port, proto) for port, proto in self.__ports}

    @property
    def readyness_poll_interval(self) -> float:
        return self.__readyness_poll_interval


def ci_fixture(dockerclient: docker.client.DockerClient,
               image: Image,
               *ports: Tuple[int, str],
               ci_check: Callable[[], bool] = ci.is_containerized_ci,
               ci_address: str = 'localhost',
               command: Optional[Union[str, List[str]]] = None,
               environment: Optional[Mapping[str, str]] = None,
               max_wait: Optional[float] = None,
               options: Optional[Mapping[str, Any]] = None,
               readyness_poll_interval: Optional[float] = None,
               ) -> Generator[Service, None, None]:
    """CI/CD compatible version of the :func:`fixture` function.

    Use this fixture if your tests will run in a CI environment capable of
    providing containers without the need to do so within the tests themselves.

    Detection of whether the tests are run within a CI system is done
    by checking if the environment variable given by the `ci_variable`
    argument is set or not (whatever its value is).

    Arguments are the same as the :func:`.fixture` function, but for two additional
    one:

    Args:
        ci_variable: the name of the variable to check to determine if the tests
            are running in a CI environment or not (default: `'CI'`).
        ci_address: the network address on which the CI systems binds container
            ports (default: `'localhost'`).

    """
    assert ci_check is not None

    if ci_check():  # Assumes code is running in CI environment.
        with FakeContainer(ci_address, *ports) as cntr:
            wait_kwargs = dict(max_wait=max_wait, readyness_poll_interval=readyness_poll_interval)
            _prune_dict(wait_kwargs)
            cntr.wait(*ports, **wait_kwargs)
            yield cntr
    else:
        yield from fixture(dockerclient,
                           image,
                           *ports,
                           command=command,
                           environment=environment,
                           max_wait=max_wait,
                           options=options,
                           readyness_poll_interval=readyness_poll_interval)


def fixture(dockerclient: docker.client.DockerClient,
            image: Image,
            *ports: Tuple[int, str],
            command: Optional[Union[str, List[str]]] = None,
            environment: Optional[Mapping[str, str]] = None,
            max_wait: Optional[float] = None,
            options: Optional[Mapping[str, Any]] = None,
            readyness_poll_interval: Optional[float] = None,
            ) -> Generator[Service, None, None]:
    """Creates a container and waits for it to start before returning it.

    Args:
        image: the image to use to create the container
    """
    with Container(image,
                   command=command,
                   dockerclient=dockerclient,
                   options=options,
                   environment=environment) as cntr:
        wait_kwargs = dict(max_wait=max_wait, readyness_poll_interval=readyness_poll_interval)
        _prune_dict(wait_kwargs)
        cntr.wait(*ports, **wait_kwargs)
        yield cntr


# vim: et:sw=4:syntax=python:ts=4:
