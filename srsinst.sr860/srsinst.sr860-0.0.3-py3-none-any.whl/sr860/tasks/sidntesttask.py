
import time
import logging
import socket
import struct
import threading

from srsgui import Task
from srsgui import IntegerInput, ListInput
from instruments.sr865.sr865 import SR865
from instruments import get_sr865


class StreamingTask(Task):
    Duration = 'duration'
    Channels = 'Channels'
    DataFormat = 'data format'
    PacketSize = 'packet size'
    Port = 'udp port'

    input_parameters = {
        Duration: IntegerInput(10, ' s', 1, 3600, 1),
        Channels: ListInput(['X', 'X, Y', 'R, Theta', 'X, Y, R, Theta'], 1),
        DataFormat: ListInput(['Float32', 'Int16']),
        PacketSize: ListInput(['1024', '512', '256', '128']),
        Port: IntegerInput(1865, '', 1024, 65535, 1)
    }

    def setup(self):
        self.logger = logging.getLogger(__file__)
        self.lia = get_sr865(self)
        
        print(self.lia.query_text('*idn?'))

        self.params = self.get_all_input_parameters()


        self.lia.stream.channel = self.params[self.Channels]
        self.lia.stream.format = self.params[self.DataFormat]
        self.lia.stream.packet_size = self.params[self.PacketSize]
        self.lia.stream.port = self.params[self.Port]


        self.logger.info('Channels: {}, Data format: {}, Packet_size: {}, Port: {}'
                         .format(list(self.lia.stream.ChannelDict.keys())[self.lia.stream.channel],
                                 list(self.lia.stream.FormatDict.keys())[self.lia.stream.format],
                                 list(self.lia.stream.PacketSizeDict.keys())[self.lia.stream.packet_size],
                                 self.lia.stream.port,
                                 )
                         )

        # Mark the time 0
        self.init_time = time.time()

    def test(self):
        while time.time() - self.init_time < self.params[self.Duration]:
            if not self.is_running():
                break

            start_time = time.time()
            for i in range(100):
                print(self.lia.query_text('*idn?'))
            finish_time = time.time()
            print('Time for 100 *idn: {}'.format(finish_time - start_time))
            break

    def cleanup(self):
        pass

