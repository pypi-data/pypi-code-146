import os
import cv2


class ImageVideoProcessor():

    def __init__(self, image_path, video_path):
        self.image_path = image_path
        self.video_path = video_path
        self.cap = cv2.VideoCapture(self.video_path)
        self.cap.set(cv2.CAP_PROP_POS_FRAMES, 0)

    def extract_frames(video_path, frames_path):
        # Load the video
        video = cv2.VideoCapture(video_path)

        # Get the video frame count
        frame_count = int(video.get(cv2.CAP_PROP_FRAME_COUNT))

        # Iterate over the frames of the video
        for i in range(frame_count):
            # Read the next frame
            ret, frame = video.read()

            # If the frame was read successfully
            if ret:
                # Save the frame to the specified location
                cv2.imwrite(f'{frames_path}/frame_{i}.jpg', frame)
            else:
                break

        # Release the video file
        video.release()

    def merge_frames_to_video(frames_path, video_path, fps=24):
        # Get the list of image files in the frames directory
        frames = [f for f in os.listdir(frames_path) if f.endswith('.jpg') or f.endswith('.png')]
        frames.sort()

        # Get the first frame to set the video dimensions
        first_frame = cv2.imread(os.path.join(frames_path, frames[0]))
        height, width, layers = first_frame.shape

        # Define the codec and create a video writer object
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        video = cv2.VideoWriter(video_path, fourcc, fps, (width, height))

        # Add the frames to the video
        for frame in frames:
            video.write(cv2.imread(os.path.join(frames_path, frame)))

        # Release the video writer
        video.release()
