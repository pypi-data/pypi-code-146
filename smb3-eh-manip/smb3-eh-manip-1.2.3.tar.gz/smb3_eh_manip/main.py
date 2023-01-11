import logging
import time
from signal import signal, SIGINT

from pygrabber.dshow_graph import FilterGraph

from smb3_eh_manip.app.controller import Controller
from smb3_eh_manip.util.logging import initialize_logging
from smb3_eh_manip.util import settings


def handler(_signum, _frame):
    global controller
    print("SIGINT or CTRL-C detected. Exiting gracefully")
    controller.terminate()
    controller = None


def print_camera_info():
    graph = FilterGraph()
    input_devices = graph.get_input_devices()
    video_capture_source = settings.get_int("video_capture_source")
    if video_capture_source == -1 or video_capture_source >= len(input_devices):
        logging.info(
            "No camera selected or invalid, please update to one of the below:"
        )
        logging.info(input_devices)
        exit()
    logging.info(f"Selected video source: {input_devices[video_capture_source]}")


def main():
    global controller
    signal(SIGINT, handler)
    initialize_logging()
    print_camera_info()
    try:
        controller = Controller()
        last_tick_duration = -1
        while controller is not None:
            start_time = time.time()
            controller.tick(last_tick_duration)
            last_tick_duration = time.time() - start_time
            logging.debug(f"Took {last_tick_duration}s to tick")
    except Exception as e:
        logging.error(f"Received fatal error: {e}")
        raise e


if __name__ == "__main__":
    main()
