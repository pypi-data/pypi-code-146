import logging
from datetime import timedelta
from typing import List, Optional, Sequence, Union  # for type hinting

from .._endpoint.ipv4.nat import NattedPort  # for type hinting
from .._endpoint.port import Port  # for type hinting

# ! FIXME - Import does not work: cyclic import dependencies!
# from .._analysis.flow_analyser import FlowAnalyser  # for type hinting


class Flow(object):
    """Base class of a flow between one and one or more ByteBlower ports."""

    __slots__ = (
        '_source',
        '_destination',
        '_name',
        '_tags',
        '_analysers',
    )

    _number = 1

    _CONFIG_ELEMENTS = (
        'source',
        'destination',
        'name',
        'analysers',
        'type',
    )

    def __init__(
            self,
            source: Union[Port, NattedPort],
            destination: Union[Port, NattedPort],
            # *args,
            name: Optional[str] = None,
            **kwargs) -> None:

        self._source = source
        self._destination = destination

        if name is not None:
            self._name = name
        else:
            self._name = 'Flow ' + str(Flow._number)

        if kwargs:
            logging.error('Unsupported keyword arguments for Flow %r: %r',
                          self._name, [
                              '{}={!r}'.format(key, value)
                              for key, value in kwargs.items()
                          ])
            raise ValueError(
                'Unsupported configuration parameters'
                f' for Flow {self._name!r}: {[key for key in kwargs]!r}')

        if self._source.failed:
            raise ValueError(
                'Cannot send from ByteBlower Port {!r} because address'
                ' configuration failed.'.format(self._source.name))

        if self._destination.failed:
            raise ValueError(
                'Cannot send to ByteBlower Port {!r} because address'
                ' configuration failed.'.format(self._destination.name))

        if self._source.is_natted and self._destination.is_natted:
            raise ValueError(
                'Cannot send between two ByteBlower Ports ({!r} <> {!r})'
                ' behind a NAT.'.format(self._source.name,
                                        self._destination.name))

        self._analysers: List[
            'byteblower_test_framework.analysis.FlowAnalyser'] = list()

        self._tags: List[str] = list()
        self.add_tag('from_' + self._source.name)
        for tag in self._source.tags:
            self.add_tag('from_' + tag)
        self.add_tag('to_' + self._destination.name)
        for tag in self._destination.tags:
            self.add_tag('to_' + tag)

        Flow._number += 1

    @property
    def source(self) -> Union[Port, NattedPort]:
        return self._source

    @property
    def destination(self) -> Union[Port, NattedPort]:
        return self._destination

    @property
    def name(self) -> str:
        return self._name

    @property
    def type(self) -> str:
        return self.__class__.__name__

    # @property
    # def analysers(self) -> Sequence[FlowAnalyser]:
    #     return self._analysers

    @property
    def config(self) -> Sequence[str]:
        configs = []

        for k in self._CONFIG_ELEMENTS:
            if k == 'analysers':
                continue

            if k == 'source' or k == 'destination':
                port: Port = getattr(self, k)
                v = port.ip
            else:
                v = getattr(self, k)
            configs.append("{k!s} = {v!s}".format(k=k, v=v))
        return configs

    def add_analyser(
            self, analyser: 'byteblower_test_framework.analysis.FlowAnalyser'
    ) -> None:
        analyser._add_to_flow(self)
        self._analysers.append(analyser)

    def apply(self, **kwargs) -> None:
        """
        .. note::
           Virtual method.
        """
        for analyser in self._analysers:
            analyser.apply()

    def process(self) -> None:
        for analyser in self._analysers:
            analyser.process()

    def updatestats(self) -> None:
        """
        .. note::
           Virtual method.
        """
        for analyser in self._analysers:
            analyser.updatestats()

    def analyse(self) -> None:
        """
        .. note::
           Virtual method.
        """
        for analyser in self._analysers:
            analyser.analyse()

    def add_tag(self, new_tag) -> None:
        new_tag = new_tag.lower()
        if new_tag not in self._tags:
            self._tags.append(new_tag)

    def wait_until_finished(self, wait_for_finish: timedelta) -> None:
        """
        .. note::
           Virtual method.
        """
        pass
