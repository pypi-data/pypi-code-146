"""Memory Class"""
import threading
import logging
import zmq
from ..constants import MEMORY_REQ_URL

class MemoryControl(threading.Thread):
    """Memoery Control Class"""

    def send_message(self):
        """Send the message"""
        task_sender = self.context.socket(zmq.PUSH)
        task_sender.connect(self.push_url)
        task_sender.send(self.control_msg.encode())

    def close(self):
        """Close the thread"""
        self.running = False

    def __init__(self, device_id: str, control_type: str, control_id: str, push_url: str, pull_url: str,context: zmq.Context) -> None:
        threading.Thread.__init__(self, daemon=True)
        self.context = context
        self.device_id = device_id
        self.mem = {}
        self.start()

    def run(self):
        socket = self.context.socket(zmq.REP)
        socket.bind(MEMORY_REQ_URL.format(self.device_id))

        while True:
            #  Wait for next request from client
            message = socket.recv_multipart()
            logging.debug("MEM Rx: %s", message)
            if len(message) == 3:
                if message[0] == b'SET':
                    self.mem[message[1]]=message[2]
                    logging.debug("MEM Tx: SET: %s, TO: %s", message[1], message[2])
                    socket.send_multipart([message[0],message[1],message[2]])
                if message[0] == b'GET':
                    logging.debug("MEM Tx: GET: %s, RTN: %s", message[1], message[1])
                    socket.send_multipart([message[0],message[1],self.mem[message[1]]])
            #  Send error reply back to client
            socket.send_multipart([b'ERROR',b'ERROR',b'ERROR'])
       