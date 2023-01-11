import argparse
import importlib.util
import math
import sys
import time
from typing import List


def print_frame(frame, height, print_char):
    """
    Prints print_char bars of height frame[x] where x is a position of the bar from left to right.

    :param frame: list of heights
    :param height: maximum height
    :param print_char: char used to represent a bar
    """
    for i in range(height, 0, -1):
        for j in range(len(frame)):
            if i <= frame[j]:
                print(print_char, end='')
            else:
                print(' ', end='')
        print()


def clear_frame(height):
    for _ in range(height):
        sys.stdout.write("\033[F\033[K")


class FrameLengthSmallerThanWidth(Exception):
    def __init__(self, fps, width):
        super().__init__(f"Width of frame is lesser than width of print line. Increase fps({fps}) or decrease "
                         f"width({width})")


def graph_frames_from_audio(data, step, width, divisor):
    """
    Interpolates values in data list by taking an average of step values.
    After processing width * step values will yield a list of width interpolated values.
    Once the data array has been processed yields final list of the remaining values if there are any.

    :param data: array of numbers representing audio data
    :param step: number of values to use for interpolation
    :param width: width of frame, number of interpolated values
    :param divisor: divide each value with this number
    :return: generator yielding a current frame
    """
    point = 0
    current_sum = 0
    current_frame = []
    for x in data:
        current_sum += int((abs(x) // divisor))
        point += 1
        if point == step:
            current_frame.append(math.ceil(current_sum / point))
            point = 0
            current_sum = 0
        if len(current_frame) == width:
            yield current_frame
            current_frame = []
    if current_frame:
        yield current_frame
    elif current_sum:
        yield [current_sum / point]


def calc_data_for_visualization(data: List[float], frame_rate: int, max_amp: float, width: int, fps: int, height: int):
    """
    Calculates all the data we need to visualize audio stream
    """
    length = len(data)
    point_interval = frame_rate // (width * fps)  # interval used for interpolation
    if point_interval == 0:
        raise FrameLengthSmallerThanWidth(fps, width)
    frame_mod = length % (point_interval * width)
    last_frame_length = frame_rate / (length % (point_interval * width)) if frame_mod != 0 else 1
    interval = 1.0 / fps
    divisor = max_amp / height
    return length, point_interval, last_frame_length, interval, divisor


def visualize(data, frame_rate: int, max_amp: float, fps=30, width=30, height=15, print_char="#", debug=False,
              sync=True):
    """
    Visualizes the data array

    :param data: array of numbers representing audio stream
    :param frame_rate: audio frame rate, number of values in the data array representing one second of audio
    :param max_amp: maximum amplitude of the audio data
    :param fps: how many frames to render each second
    :param width: width of rendered frames, 1 unit represents one char length in terminal
    :param height: height of rendered frames, 1 unit represents one char length in terminal
    :param print_char: char used to render frames
    :param debug: if true will print number of skipped frames
    :param sync: if true will keep the graphical representation in sync with audio, else will just print graphical
    frames as they are calculated
    :return: number of skipped frames
    """
    length, point_interval, last_frame_length, interval, divisor = \
        calc_data_for_visualization(data, frame_rate, max_amp, width, fps, height)
    skipped_frames = 0
    audio_start = time.time()
    print_frame([0] * width, height, " ")
    for i, f in enumerate(graph_frames_from_audio(data, point_interval, width, divisor)):
        clear_frame(height)
        print_frame(f, height, print_char)
        frame_length = last_frame_length if i == length - 1 else 1  # 1 denotes full frame
        end_time = audio_start + ((i + 1 * frame_length) * interval)
        sleep_for = end_time - time.time()
        if sync and sleep_for > 0:
            time.sleep(sleep_for)
        else:
            skipped_frames += 1
    if debug:
        print(skipped_frames)
    return skipped_frames


def open_file(filename, file_type):
    spec = importlib.util.find_spec("pydub")
    if spec is None:
        raise ImportError("pydub is not installed, install pydub to run this program")
    from pydub import AudioSegment
    if file_type == "mp3":
        return AudioSegment.from_mp3(filename)
    elif file_type == "wav":
        return AudioSegment.from_wav(filename)
    elif file_type == "flv":
        return AudioSegment.from_flv(filename)
    elif file_type == "ogg":
        return AudioSegment.from_ogg(filename)
    elif file_type == "raw":
        return AudioSegment.from_raw(filename)


def run(filename, file_type="mp3", fps=30, width=30, height=15, print_char="#", debug=False, sync=True):
    audio = open_file(filename, file_type)
    data = audio.get_array_of_samples()[0::2]
    visualize(data, audio.frame_rate, audio.max_possible_amplitude, fps, width, height, print_char, debug, sync)


def main():
    parser = argparse.ArgumentParser(prog="visualizer", description="visualize audio")
    parser.add_argument("filename", help="path to audio file")
    parser.add_argument("-t", "--type", help="file type of the audio file", default="mp3")
    parser.add_argument("-f", "--fps", help="frames per second for the graphical representation of audio",
                        default=30, type=int)
    parser.add_argument("-w", "--width", help="width of graphical representation of audio", default=30, type=int)
    parser.add_argument("-he", "--height", help="height of the graphical representation of audio", default=15, type=int)
    parser.add_argument("-c", "--char", help="char used to represent graph point", default="#", type=lambda x: x[0])
    parser.add_argument("-d", "--debug", help="prints the number of skipped frames", action="store_true")
    parser.add_argument("-ns", "--nosync", help="do not sync graph with audio", action="store_true")

    args = parser.parse_args()
    run(args.filename, args.type, args.fps, args.width, args.height, args.char, args.debug, not args.nosync)


if __name__ == "__main__":
    main()
