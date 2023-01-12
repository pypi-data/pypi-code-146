from datetime import timedelta  # for type hinting
from typing import List, Optional, Sequence, Union  # for type hinting

from byteblowerll.byteblower import Stream as TxStream  # for type hinting

from .._endpoint.ipv4.nat import NattedPort  # for type hinting
from .._endpoint.port import Port  # for type hinting
from .flow import Flow
from .frame import Frame  # for type hinting
from .imix import Imix  # for type hinting

DEFAULT_FRAME_RATE: float = 100.0
INFINITE_NUMBER_OF_FRAMES: int = -1
DEFAULT_NUMBER_OF_FRAMES: int = INFINITE_NUMBER_OF_FRAMES


class FrameBlastingFlow(Flow):

    __slots__ = (
        '_stream',
        '_frame_rate',
        '_number_of_frames',
        '_imix',
        '_frame_list',
    )

    _CONFIG_ELEMENTS = Flow._CONFIG_ELEMENTS + (
        'frame_rate',
        'number_of_frames',
        'initial_time_to_wait',
    )

    def __init__(
            self,
            source: Union[Port, NattedPort],
            destination: Union[Port, NattedPort],
            name: Optional[str] = None,
            frame_rate: Optional[float] = DEFAULT_FRAME_RATE,  # [fps]
            number_of_frames: Optional[int] = DEFAULT_NUMBER_OF_FRAMES,
            duration: Optional[Union[timedelta, float,
                                     int]] = None,  # [seconds]
            initial_time_to_wait: Optional[Union[timedelta, float,
                                                 int]] = None,  # [seconds]
            frame_list: Optional[Sequence[Frame]] = None,
            imix: Optional[Imix] = None,
            **kwargs) -> None:
        """Create a Frame Blasting flow.

        :param source: Sending port of the voice stream
        :type source: Union[Port, NattedPort]
        :param destination: Receiving port of the voice stream
        :type destination: Union[Port, NattedPort]
        :param name: Name of this Flow, defaults to auto-generated name
           when set to ``None``.
        :type name: str, optional
        :param frame_rate: Rate at which the frames are transmitted
           (in frames per second), defaults to :const:`DEFAULT_FRAME_RATE`
        :type frame_rate: float, optional
        :param number_of_frames: Number of frames to transmit,
           defaults to :const:`DEFAULT_NUMBER_OF_FRAMES`
        :type number_of_frames: int, optional
        :param duration: Duration of the flow in seconds,
           defaults to None (use number_of_frames instead)
        :type duration: Union[timedelta, float, int], optional
        :param initial_time_to_wait: Initial time to wait to start the flow.
           In seconds, defaults to None (start immediately)
        :type initial_time_to_wait: Union[timedelta, float, int], optional
        :param frame_list: List of frames to transmit,
           mutual exclusive with ``imix``, defaults to None
        :type frame_list: Sequence[Frame], optional
        :param imix: Imix definition of frames to transmit,
           mutual exclusive with ``frame_list``, defaults to None
        :type imix: Imix, optional
        :raises ValueError: When both ``imix`` and ``frame_list`` are given
           or when none of both is given.
        """
        super().__init__(source, destination, name=name, **kwargs)

        self._frame_rate = frame_rate
        if duration is not None:
            if isinstance(duration, timedelta):
                # Convert to float
                duration = duration.total_seconds()
            # else:
            #     # Already float/int:
            #     duration = duration or 0
            self._number_of_frames = int(duration * frame_rate)
        else:
            self._number_of_frames = number_of_frames

        if isinstance(initial_time_to_wait, timedelta):
            # Convert to float
            initial_time_to_wait = initial_time_to_wait.total_seconds()
        # else:
        #     # Either already float/int or None:
        #     pass

        self._imix = imix

        if self._imix and frame_list:
            raise ValueError(f'Flow {self._name!r}: Please provide'
                             ' either IMIX or frame list but not both.')
        if self._imix:
            frame_list = self._imix._generate(self._source)

        if not frame_list:
            raise ValueError(f'Flow {self._name!r}: Please provide at least'
                             ' either IMIX or frame list.')
        # Create the stream
        self._stream: TxStream = self._source.bb_port.TxStreamAdd()
        if initial_time_to_wait is not None:
            self._stream.InitialTimeToWaitSet(
                int(initial_time_to_wait * 1000000000))

        self._frame_list: List[Frame] = list()
        for frame in frame_list:
            frame._add(self._source, self._destination, self._stream)
            self._frame_list.append(frame)

    @property
    def frame_rate(self) -> float:
        return self._frame_rate

    @property
    def number_of_frames(self) -> int:
        return self._number_of_frames

    @property
    def initial_time_to_wait(self) -> int:
        return self._stream.InitialTimeToWaitGet()

    # def add_frame(self, frame: Frame) -> None:
    #     frame._add(self._source, self._destination, self._stream)
    #     self._frame_list.append(frame)

    def apply(self, duration: Optional[timedelta] = None, **kwargs) -> None:
        # if initial_time_to_wait is set, subtract this wait time
        # from the scenario duration
        if isinstance(self.initial_time_to_wait, timedelta):
            duration -= self.initial_time_to_wait

        if self.number_of_frames == INFINITE_NUMBER_OF_FRAMES:
            self._number_of_frames = int(duration.total_seconds() *
                                         self.frame_rate)

        self._stream.InterFrameGapSet(int(1000000000 / self._frame_rate))
        self._stream.NumberOfFramesSet(self._number_of_frames)
        super().apply(**kwargs)
