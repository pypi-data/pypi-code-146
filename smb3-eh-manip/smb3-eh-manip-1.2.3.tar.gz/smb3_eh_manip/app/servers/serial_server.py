import logging
import serial
import time
from multiprocessing import Process, Value
from signal import signal, SIGINT

from smb3_eh_manip.util import events, settings
from smb3_eh_manip.util.logging import initialize_logging

LOAD_FRAME_THRESHOLD = 3  # anything higher than this number is considered a load frame instead of lag frame
SERIAL_TIMEOUT = float(settings.get("serial_timeout", fallback="0.1"))
SERIAL_PORT = settings.get("serial_port", fallback="COM4")
SERIAL_BAUDRATE = settings.get_int("serial_baudrate", fallback=115200)
SERIAL_PAYLOAD_SIZE = settings.get_int("serial_payload_size", fallback=2)
SERIAL_LATENCY_MS = settings.get_int("serial_latency_ms", fallback=16)


def handler(_signum, _frame):
    global running
    print("SIGINT or CTRL-C detected. Exiting gracefully")
    running = False


def server_process(lag_frames_observed: Value, load_frames_observed: Value):
    initialize_logging(console_log_level="DEBUG", filename="restrospy_server.log")
    arduino = serial.Serial(
        port=SERIAL_PORT, baudrate=SERIAL_BAUDRATE, timeout=SERIAL_TIMEOUT
    )
    while True:
        data = arduino.readline().strip()
        if len(data) != SERIAL_PAYLOAD_SIZE:
            logging.debug(f"Data frame not sized properly {len(data)}")
            continue
        timestamp_diff = (data[-1] << 8) + data[-2]
        packet_lag_frames = round(timestamp_diff / settings.NES_MS_PER_FRAME) - 1
        if packet_lag_frames < 0:
            logging.debug(
                f"We think we got {packet_lag_frames} frames, correcting to 0. timestamp_diff: {timestamp_diff}"
            )
            packet_lag_frames = 0
        if packet_lag_frames:
            if packet_lag_frames > LOAD_FRAME_THRESHOLD:
                logging.debug(f"Observed {packet_lag_frames} load frames")
                total = load_frames_observed.value + packet_lag_frames
                with load_frames_observed.get_lock():
                    load_frames_observed.value = total
            else:
                logging.debug(f"Observed {packet_lag_frames} lag frames")
                total = lag_frames_observed.value + packet_lag_frames
                with lag_frames_observed.get_lock():
                    lag_frames_observed.value = total
        time.sleep(0.001)


class SerialServer:
    def __init__(self):
        self.lag_frames_observed_value = Value("i", 0)
        self.lag_frames_observed = 0
        self.load_frames_observed_value = Value("i", 0)
        self.load_frames_observed = 0
        self.server_process = Process(
            target=server_process,
            args=(
                self.lag_frames_observed_value,
                self.load_frames_observed_value,
            ),
        )
        self.server_process.daemon = True
        self.server_process.start()

    def tick(self, current_frame=0.0):
        new_lag_frames_observed = (
            self.lag_frames_observed_value.value - self.lag_frames_observed
        )
        new_load_frames_observed = (
            self.load_frames_observed_value.value - self.load_frames_observed
        )
        self.lag_frames_observed += new_lag_frames_observed
        self.load_frames_observed += new_load_frames_observed
        if new_lag_frames_observed or new_load_frames_observed:
            events.emit(
                self,
                events.LagFramesObserved(
                    current_frame - (SERIAL_LATENCY_MS / settings.NES_MS_PER_FRAME),
                    new_lag_frames_observed,
                    new_load_frames_observed,
                ),
            )

    def reset(self):
        self.lag_frames_observed = 0
        with self.lag_frames_observed_value.get_lock():
            self.lag_frames_observed_value.value = 0
        self.load_frames_observed = 0
        with self.load_frames_observed_value.get_lock():
            self.load_frames_observed_value.value = 0


if __name__ == "__main__":
    global running
    running = True
    signal(SIGINT, handler)
    initialize_logging(
        filename="serial_server.log",
        file_log_level="DEBUG",
        console_log_level="DEBUG",
    )
    server = SerialServer()
    while running:
        lag_frame_detect_start = time.time()
        server.tick()
        detect_duration = time.time() - lag_frame_detect_start
        if detect_duration > 0.002:
            logging.info(f"Took {detect_duration}s detecting lag frames")
