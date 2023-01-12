"""
This class implements utils that will help to generate a source dataset from a videos directory

Author: Eric Canas.
Github: https://github.com/Eric-Canas
Email: eric@ericcanas.com
Date: 22-07-2022
"""
from vid2info.utils.user_interaction import ask_user
from vid2info.video.video_reader import VideoReader
from training_tools.config import DEFAULT_TRAIN_DIR, DEFAULT_RAW_VIDEOS_DIR, DO_YOU_WANT_TO_REMOVE_FOLDER_CONTENT
from training_tools.dataset_generation.config import TAKE_IMAGE_EVERY_N_SECONDS, ACCEPTED_VIDEO_EXTENSIONS, DEFAULT_IMAGE_EXTENSION
import os
from shutil import rmtree
import cv2
from tqdm import tqdm

def extract_images_from_video(videos_folder: str = DEFAULT_RAW_VIDEOS_DIR, output_dir: str = DEFAULT_TRAIN_DIR,
                              take_image_every_n_seconds: float | int = TAKE_IMAGE_EVERY_N_SECONDS,
                              image_format = DEFAULT_IMAGE_EXTENSION) -> bool:
    """
    Extract images from every video in the videos_folder and save them in the output_dir.
    One image is taken every take_image_every_n_seconds seconds.
    :param videos_folder: str. The folder where the videos are stored.
    :param output_dir: str. The folder where the images will be saved.
    :param take_image_every_n_seconds: float | int. The number of seconds between each image. Default is
            TAKE_IMAGE_EVERY_N_SECONDS.

    :return: True if the extraction was successful and False otherwise.
    """
    assert os.path.isdir(videos_folder), f"videos_folder {videos_folder} does not exist"
    assert take_image_every_n_seconds > 0, f"take_image_every_n_seconds is not positive. Got {take_image_every_n_seconds}"
    videos_in_folder = tuple(video for video in os.listdir(videos_folder)
                             if os.path.splitext(video)[-1] in ACCEPTED_VIDEO_EXTENSIONS)
    assert len(videos_in_folder) > 0, f"videos_folder {videos_folder} does not contain any video"
    assert len(videos_in_folder) == len(set(video.replace(" ", "") for video in videos_in_folder)), \
        f"videos_folder {videos_folder} contains duplicates when spaces are removed"
    if os.path.isdir(output_dir):
        if len(os.listdir(output_dir)) > 0:
            # Ask the user if he wants to delete the output directory
            remove_content = ask_user(question=DO_YOU_WANT_TO_REMOVE_FOLDER_CONTENT.format(output_dir))
            if remove_content:
                rmtree(output_dir)
                os.mkdir(output_dir, mode=0o777)
            else:
                print("Aborting dataset generation...")
                return False
    else:
        os.mkdir(output_dir, mode=0o777)
    img_params = (cv2.IMWRITE_JPEG_QUALITY, 100) if image_format.lower().endswith("jpg") or \
                                                    image_format.lower().endswith("jpeg") else ()
    for video_file in videos_in_folder:
        video = VideoReader(video_path=os.path.join(videos_folder, video_file),
                            simulated_frame_rate=1//take_image_every_n_seconds)
        img_name = f"{os.path.splitext(video_file)[0].replace(' ', '')}-"+"{time}s" +f"{image_format}".replace(" ", "")
        for frame in tqdm(video):
            img_time = str(round(video.current_timestamp_seconds, ndigits=2)).replace(".", "_")
            img_path = os.path.join(output_dir, img_name.format(time=img_time))
            cv2.imwrite(filename=img_path, img=frame, params=img_params)

    return True


