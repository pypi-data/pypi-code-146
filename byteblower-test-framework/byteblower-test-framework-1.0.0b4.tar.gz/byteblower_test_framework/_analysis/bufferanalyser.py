import logging
from datetime import datetime, timedelta

from pandas import DataFrame, concat

from .flow_analyser import FlowAnalyser
from .plotting.generic_chart import GenericChart


class BufferAnalyser(FlowAnalyser):
    """Analyse a video buffer over time.

    The analyser provides buffer state, incoming and outgoing data
    over time. It analyses the initial wait time for the video to start
    playing out.

    This analyser is intended for use with a :class:`~.traffic.VideoFlow`.

    Supports:

    * Analysis of a single flow

    .. warning::
       Does not support aggregation data from multiple flows
       (via :class:`~.analysis.AnalyserAggregator`).
    """

    # TODO - Cleanup code and define slots
    # __slots__ = (
    # )

    def __init__(
            self,
            buffer_size: int,
            play_goal_size: int,
            max_initial_wait_time: timedelta = timedelta(seconds=5),
    ) -> None:
        """Create the video buffer over time analyser.

        :param buffer_size: Size of the video buffer in Bytes.
        :type buffer_size: int
        :param play_goal_size:
           .. todo::
              Provide documentation for this parameter.
        :type play_goal_size: int
        :param max_initial_wait_time: Maximum allowed time to wait until
           the video starts to play, defaults to timedelta(seconds=5)
        :type max_initial_wait_time: timedelta, optional
        """
        super().__init__('Buffer analyser')
        self.buffer_size_max = buffer_size
        self.buffer_size: int = 0
        self.buffer_filled: int = 0
        self.buffer_consumed: int = 0
        # We can only consume if the buffer has reached a certain level.
        if not play_goal_size:
            self.buffer_consumable = True
        else:
            self.buffer_consumable = False
        self.play_goal_size = play_goal_size
        self.gap_start = None
        self.df_buffer = DataFrame(columns=[
            "Buffer state",
            "Buffer incoming",
            "Buffer outgoing",
        ])
        self.df_buffer_gap = DataFrame(columns=["Start", "Stop"])
        # Stats about the initial start time
        self.test_start = None
        self.play_start = None
        self.max_initial_wait_time = max_initial_wait_time
        self._log = ''

    def _initialize(self) -> None:
        # Nothing to do
        pass

    def process(self) -> None:
        # if self.buffer_size == 0:
        #     # Buffer is empty!
        #     if self.gap_start is None:
        #         self.gap_start = datetime.now()
        #         self._set_result(False)
        #     else:
        #         if self.gap_start is not None:
        #             df_buffer_gap_update = DataFrame({
        #                 "Start": self.gap_start,
        #                 "Stop": datetime.now()
        #             })
        #             self.df_buffer_gap = concat([self.df_buffer_gap, df_buffer_gap_update], ignore_index=True)
        #             self.gap_start = None
        if self.test_start is None:
            self.test_start = datetime.now()

    def updatestats(self) -> None:
        logging.debug("Buffer size: %s, filled %s, consumed %s",
                      self.buffer_size, self.buffer_filled,
                      self.buffer_consumed)
        self.df_buffer.loc[datetime.now()] = [
            self.buffer_size,
            self.buffer_filled,
            self.buffer_consumed,
        ]
        self.buffer_filled = 0
        self.buffer_consumed = 0

    def buffer_fill(self, size: int) -> None:
        logging.debug("Filling buffer of size %s with size %s",
                      self.buffer_size, size)
        previous = self.buffer_size
        self.buffer_size += size
        if self.buffer_size > self.buffer_size_max:
            self.buffer_size = self.buffer_size_max
        self.buffer_filled += self.buffer_size - previous
        if not self.buffer_consumable:
            if self.buffer_size > self.play_goal_size:
                if self.play_start is None:
                    self.play_start = datetime.now()
                self.buffer_consumable = True
                if self.gap_start is not None:
                    df_buffer_gap_update = DataFrame({
                        "Start": self.gap_start,
                        "Stop": datetime.now()
                    })
                    self.df_buffer_gap = concat(
                        [self.df_buffer_gap, df_buffer_gap_update],
                        ignore_index=True)
                    self.gap_start = None
        # else:
        #     logging.debug(
        #         "Buffer is not consumable yet: size %s vs start_goal %s",
        #         self.buffer_size, self.play_goal_size)
        # logging.debug("Buffer is now filled to %s, while max is %s",
        #               self.buffer_size, self.buffer_size_max)

    def buffer_consume(self, size: int) -> None:
        # logging.debug("Trying to consume %d bytes", size)
        if self.buffer_consumable:
            if self.play_start is None:
                if self.test_start is None:
                    self.test_start = datetime.now()
                self.play_start = datetime.now()

            previous = self.buffer_size
            self.buffer_size -= size
            if self.buffer_size < 0:
                self.buffer_size = 0
                self.gap_start = datetime.now()
                self.buffer_consumable = False
                self._set_result(False)
            self.buffer_consumed += previous - self.buffer_size
            # logging.debug("Consumed %d bytes.", previous - self.buffer_size)

    @property
    def size(self) -> int:
        return self.buffer_size

    @property
    def size_max(self) -> int:
        return self.buffer_size_max

    def analyse(self) -> None:
        # Parameters to pass this test:
        #   Packet loss: ?
        if self.gap_start is not None:
            df_buffer_gap_update = DataFrame({
                "Start": self.gap_start,
                "Stop": datetime.now()
            })
            self.df_buffer_gap = concat(
                [self.df_buffer_gap, df_buffer_gap_update], ignore_index=True)
        if len(self.df_buffer_gap.index) > 0:
            if len(self.df_buffer_gap.index) == 1:
                self._log = "There is one gap detected."
            else:
                self._log = "There are {} gaps detected.".format(
                    len(self.df_buffer_gap.index))
        else:
            if self.play_start is None:
                self._log = "Never started to play the video."
                self._set_result(False)
            else:
                self._log = "No gaps detected."
                self._set_result(True)
        # Play start
        if self.play_start is None or self.test_start is None:
            logging.warning(
                "No start analyse: play_start: %s and test_start: %s",
                self.play_start, self.test_start)
            return

        initial_wait = self.play_start - self.test_start
        if initial_wait > self.max_initial_wait_time:
            self._log += \
                "Initial wait time was larger than {} seconds: {}s".format(
                    self.max_initial_wait_time.total_seconds(),
                    initial_wait.total_seconds())
            self._set_result(False)
        else:
            self._log += \
                "Initial wait time was smaller than {} seconds: {}s".format(
                    self.max_initial_wait_time.total_seconds(),
                    initial_wait.total_seconds())

    @property
    def log(self) -> str:
        """Return the summary log text.

        .. note::
           Used for unit test report.

        :return: Summary log text.
        :rtype: str
        """
        return self._log

    def render(self) -> str:
        result = "<pre>" + self._log + "</pre>"
        df_state = self.df_buffer[["Buffer state"]]
        df_incoming = self.df_buffer[["Buffer incoming"]]
        df_outgoing = self.df_buffer[["Buffer outgoing"]]

        chart = GenericChart(
            "Video buffer timeline",
            x_axis_options={"type": "datetime"},
            chart_options={"zoomType": "x"},
        )

        chart.add_series(list(df_state.itertuples(index=True)), "line",
                         "Buffer state", "Datasize", "byte")
        chart.add_series(
            list(df_incoming.itertuples(index=True)),
            "line",
            "Buffer incoming",
            "Dataspeed",
            "byte/s",
        )
        chart.add_series(
            list(df_outgoing.itertuples(index=True)),
            "line",
            "Buffer outgoing",
            "Dataspeed",
            "byte/s",
        )
        result += chart.plot()
        return result
