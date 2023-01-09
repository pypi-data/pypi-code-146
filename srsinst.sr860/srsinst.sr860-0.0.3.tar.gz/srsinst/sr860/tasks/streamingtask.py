
import time
import logging
import socket

import numpy as np
from  struct import unpack_from

from srsgui import Task
from srsgui import IntegerInput, FloatInput, ListInput

from instruments import get_sr865

from plots.twobytwosharexplot import TwoByTwoShareXPlot


class StreamingTask(Task):
    Duration = 'duration'
    Channels = 'Channels'
    DataFormat = 'data format'
    PacketSize = 'packet size'
    Rate = 'rate divider'
    Port = 'udp port'

    input_parameters = {
        Duration: IntegerInput(3600, ' s', 1, 360000, 1),
        Channels: ListInput(['X', 'X, Y', 'R, Theta', 'X, Y, R, Theta'], 1),
        DataFormat: ListInput(['Float32', 'Int16']),
        PacketSize: ListInput(['1024', '512', '256', '128']),
        Rate: IntegerInput(4, '  (1/2^n) ', 0, 20, 1),
        Port: IntegerInput(8086, '', 1024, 65535, 1)
    }

    def setup(self):
        self.logger = logging.getLogger(__file__)
        self.lia = get_sr865(self)
        print(self.lia.query_text('*idn?'))

        self.params = self.get_all_input_parameters()

        self.lia.stream.enable = False
        self.lia.stream.option = 2
        self.lia.stream.channel = self.params[self.Channels]
        self.lia.stream.format = self.params[self.DataFormat]
        self.lia.stream.packet_size = self.params[self.PacketSize]
        self.lia.stream.rate = self.params[self.Rate]
        self.lia.stream.port = self.params[self.Port]

        self.max_rate = self.lia.stream.max_rate
        self.sample_rate = self.max_rate / 2 ** self.lia.stream.rate
        self.packet_size = int(list(self.lia.stream.PacketSizeDict.keys())[self.lia.stream.packet_size])
        self.logger.info('Channels: {}, Data format: {}, Packet_size: {}, Rate: {:.3f} Hz, Port: {}'
                         .format(list(self.lia.stream.ChannelDict.keys())[self.lia.stream.channel],
                                 list(self.lia.stream.FormatDict.keys())[self.lia.stream.format],
                                 self.packet_size,
                                 self.sample_rate,
                                 self.lia.stream.port,
                                 )
                         )

        self.plot = TwoByTwoShareXPlot(self.figure)

        # Mark the time 0
        self.init_time = time.time()

    def test(self):
        if self.params[self.Channels] == 0:
            raise ValueError('Channel X is not allowed,Choose other multiple channels')

        self.last_p_id = 0
        self.lia.stream.start()
        try:
            while time.time() - self.init_time < self.params[self.Duration]:
                if not self.is_running():
                    break

                block, p_id = self.lia.stream.receive_packet()
                self.plot.add_data_block(*block)

                if self.last_p_id and p_id - self.last_p_id > 1:
                    self.logger.warning('{} missing packet(s) before ID:{}'
                                        .format(p_id - self.last_p_id - 1, p_id))
                self.last_p_id = p_id
                self.notify_data_available()
        except Exception as e:
            self.logger.error(e)

    def update(self, data):
        if self.plot.request_plot_update():
            self.request_figure_update()

    def cleanup(self):
        self.lia.stream.stop()
