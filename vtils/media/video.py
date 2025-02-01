import os
from typing import List

import click
import cv2
import numpy as np
from vtils.media.frame import resize_frames, save_frames_to_directory

def video_to_frames(video_path: str) -> List:
    """
    Extracts frames from a video file.

    Parameters:
        video_path (str): The path to the video file.

    Returns:
        list: A list of frames extracted from the video.
    """
    # Open the video file
    cap = cv2.VideoCapture(video_path)

    # Check if the video was opened successfully
    if not cap.isOpened():
        raise ValueError(f"Error opening video file: {video_path}")

    frames = []
    frame_time = []

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # Convert BGR to RGB and append the frame to the list
        frames.append(cv2.cvtColor(frame, cv2.COLOR_RGB2BGR))

        # record frame's time
        frame_time.append(cap.get(cv2.CAP_PROP_POS_MSEC) / 1000.0)

    # Release the video capture object
    cap.release()

    return frames, np.array(frame_time)


# Input video path and output a list of frames saved to disc
@click.command()
@click.option('video_path', '-vp', type=click.Path(exists=True))
@click.option('output_dir', '-od', type=click.Path())
@click.option('target_height', '-th', default=480, type=int)
@click.option('target_width', '-tw', default=640, type=int)
def main(video_path: str, output_dir: str, target_height:int, target_width:int):
    """
    Extract frames from a video file and save them to the specified directory.

    VIDEO_PATH: Path to the input video file.
    OUTPUT_DIR: Directory where the extracted frames will be saved.
    """
    # Ensure the output directory exists
    os.makedirs(output_dir, exist_ok=True)

    # Extract frames from the video
    frames = video_to_frames(video_path)
    frames = resize_frames(frames, target_height = target_height, target_width = target_width)

    # Save each frame to the output directory
    save_frames_to_directory(frames=frames, output_dir=output_dir)

if __name__ == '__main__':
    main()