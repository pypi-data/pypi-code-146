import base64
import logging

import blosc
import numpy as np

from gsdbs.dbclient import GSDBS


def gsNpCompressBase64WithShape(frame):
    bytes_array = frame.tostring()
    zframe = blosc.compress(bytes_array)
    b64frame = base64.b64encode((zframe))
    return b64frame.decode('utf-8'), frame.shape[0], frame.shape[1], frame.shape[2]


def gsNpCompressWithShape(frame):
    bytes_array = frame.tostring()
    zframe = blosc.compress(bytes_array)
    return zframe, frame.shape[0], frame.shape[1], frame.shape[2]


def gsNumpyDecompressBase64(b64frame, w, h, d):
    zframe = base64.b64decode(b64frame.encode('utf-8'))
    frame = np.frombuffer(blosc.decompress(zframe, True), dtype=np.uint8)
    frame.shape = (int(w), int(h), int(d))
    return frame


def gsNumpyDecompress(zframe, w, h, d):
    frame = np.frombuffer(blosc.decompress(zframe, True), dtype=np.uint8)
    frame.shape = (int(w), int(h), int(d))
    return frame


def gsNpToBytesWithShape(frame):
    return frame.tobytes(), frame.shape[0], frame.shape[1], frame.shape[2]


def gsBytesToNPArray(frame):
    nparray = np.frombuffer(frame[0], dtype=np.uint8)
    nparray.shape = (int(frame[1]), int(frame[2]), int(frame[3]))
    return nparray


def handleparametermissing(request, *args):
    for parameter in args:
        if request.get(parameter) is None:
            raise ValueError('Missing paramter: ' + parameter)


class LogDBHandler(logging.Handler):
    '''
    Customized logging handler that puts logs to the database.
    pymssql required
    '''

    def __init__(self, gsdbs: GSDBS):
        logging.Handler.__init__(self)
        self.gsdbs = gsdbs

    def emit(self, record):
        # Set current time
        # Clear the log message so it can be put to db via sql (escape quotes)
        self.log_msg = record.msg
        self.log_msg = self.log_msg.strip()
        self.log_msg = self.log_msg.replace('\'', '\'\'')
        logrequest = f"""
            mutation{{
            addDTable(
                dtablename:"gslog",
                superDTable:[DTABLE],
                sriBuildInfo:"${{jobid}}",
                dataLinks:[{{ alias:"jobid",locale:DE,superPropertyURI:DYNAMIC_DATALINK,DataType:STRING}},
                {{ alias:"groupid",locale:DE,superPropertyURI:DYNAMIC_DATALINK,DataType:STRING}},
                {{ alias:"computingstep",locale:DE,superPropertyURI:DYNAMIC_DATALINK,DataType:STRING}},
                {{ alias:"cnode",locale:DE,superPropertyURI:DYNAMIC_DATALINK,DataType:STRING}},
                {{ alias:"level",locale:DE,superPropertyURI:DYNAMIC_DATALINK,DataType:STRING}},
                {{ alias:"message",locale:DE,superPropertyURI:DYNAMIC_DATALINK,DataType:STRING}}],
                data:[
                    ["jobid","groupid","computingstep","cnode","level","message"]
                    ["{self.gsdbs.credentials["cnode"]}","","","{self.gsdbs.credentials["cnode"]}","{str(record.levelname)}","{str(self.log_msg)}"]
                ]
            )
        }}
        """
        self.gsdbs.executeStatementSync(logrequest)
