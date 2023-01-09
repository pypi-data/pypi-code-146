
import socket
from struct import unpack_from
import numpy as np

from srsgui.inst.component import Component
from srsgui.inst.commands import Command, GetCommand,\
                                 BoolCommand, BoolGetCommand,\
                                 IntCommand, IntGetCommand, IntSetCommand,\
                                 FloatCommand, FloatSetCommand, FloatGetCommand

from srsgui.inst.indexcommands import IndexCommand, IndexGetCommand, \
                                      IntIndexCommand, IntIndexGetCommand, \
                                      BoolIndexCommand, BoolIndexGetCommand,\
                                      FloatIndexCommand


class Stream(Component):
    ChannelDict = {
        'X':  0,
        'XY': 1,
        'RT': 2,
        'XYRT': 3
    }

    FormatDict = {
        'float32': 0,
        'int16': 1
    }

    PacketSizeDict = {
        1024: 0,
        512:  1,
        256:  2,
        128:  3
    }

    OptionDict = {
        'little_endian': 1,
        'data_integrity_checking': 2
    }

    channel = IntCommand('STREAMCH')
    max_rate = FloatGetCommand('STREAMRATEMAX')
    rate = IntCommand('STREAMRATE')
    format = IntCommand('STREAMFMT')
    packet_size = IntCommand('STREAMPCKT')
    port = IntCommand('STREAMPORT')
    option = IntCommand('STREAMOPTION')
    enable = BoolCommand('STREAM')

    def _prepare(self):
        self.udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.udp_socket.bind(('', self.port))
        self.timeout = 10
        self.udp_socket.settimeout(self.timeout)
        self.prepared_channel = self.channel

        self.prepared_packet_size = int(list(Stream.PacketSizeDict.keys())[self.packet_size])
        self.unpack_format = '>{}h'.format(self.prepared_packet_size // 2) if self.format else \
                             '>{}f'.format(self.prepared_packet_size // 4)

    def receive_packet(self):
        buffer, _ = self.udp_socket.recvfrom(self.prepared_packet_size + 4)
        packet_number = unpack_from('>I', buffer)[0] & 0xffff
        vals = unpack_from(self.unpack_format, buffer, 4)

        arr = None
        if self.prepared_channel == 0:
            arr = np.array(vals)

        elif self.prepared_channel == 1:
            rows = len(vals) // 2
            mat = np.transpose(np.reshape(vals, (rows, 2)))
            r = np.sqrt(np.square(mat[0]) + np.square(mat[1]))
            th = 180.0 / np.pi * np.arctan2(mat[1], mat[0])
            arr = np.append(np.append(mat, np.reshape(r, (1, rows)), axis=0),
                            np.reshape(th, (1,rows)), axis=0)

        elif self.prepared_channel == 2:
            rows = len(vals) // 2
            mat = np.transpose(np.reshape(vals, (rows, 2)))
            angle = np.pi / 180.0 * mat[1]
            x = mat[0] * np.cos(angle)
            y = mat[0] * np.sin(angle)
            arr = np.append(np.append(np.reshape(x, (1, rows)),
                                      np.reshape(y, (1, rows)), axis=0),
                            mat, axis=0)

        elif self.prepared_channel == 3:
            row = len(vals) // 4
            arr = np.transpose(np.reshape(vals, (row, 4)))

        return arr, packet_number

    def start(self):
        self._prepare()
        self.enable = True

    def stop(self):
        self.enable = False
        self.udp_socket.close()


class Auto(Component):
    def set_phase(self):
        self.comm.send('APHS')

    def set_range(self):
        self.comm.send('ARNG')

    def set_scale(self):
        self.comm.send('ASCL')
