import numpy as np
import cv2
import os

def resize_frames(frames: list, target_height: int = 480, target_width: int = 640) -> list:
    """
    Resizes a list of frames to the specified target height and width.

    Args:
        frames (List): A list of frames (images) to be resized.
        target_height (int): The desired height for the resized frames. Default is 480.
        target_width (int): The desired width for the resized frames. Default is 640.

    Returns:
        List: A list of frames resized to the specified dimensions.
    """
    return [resize_frame(frame, target_height, target_width) for frame in frames]


def resize_frame(frame: np.ndarray, target_height: int = 480, target_width: int = 640) -> np.ndarray:
    """
    Resize an image frame to fit within specified dimensions while maintaining the aspect ratio.
    Pads the resized image to exactly match the target dimensions.

    Args:
      frame: A 2D or 3D numpy array representing the image.
      target_height: Desired height of the output image.
      target_width: Desired width of the output image.
    Returns:
      A numpy array representing the resized and padded image with the specified target dimensions.
    """
    original_height, original_width = frame.shape[:2]

    # Calculate the scaling factor
    scale = min(target_width / original_width, target_height / original_height)

    # Resize the frame
    new_dimensions = (int(original_width * scale), int(original_height * scale))
    resized_frame = cv2.resize(frame, new_dimensions)

    # Calculate padding
    pad_vertical = target_height - resized_frame.shape[0]
    pad_horizontal = target_width - resized_frame.shape[1]
    pad_top, pad_bottom = pad_vertical // 2, pad_vertical - pad_vertical // 2
    pad_left, pad_right = pad_horizontal // 2, pad_horizontal - pad_horizontal // 2

    # Pad the resized frame
    padded_frame = cv2.copyMakeBorder(
        resized_frame,
        pad_top, pad_bottom, pad_left, pad_right,
        cv2.BORDER_CONSTANT, value=[0, 0, 0]
    )
    return padded_frame


def save_frames_to_directory(frames: list[np.ndarray], output_dir: str):
    """
    Save a list of frames to the specified directory.

    Args:
        frames (List[np.ndarray]): A list of frames to be saved.
        output_dir (str): The directory where the frames will be saved.
    """
    # Ensure the output directory exists
    os.makedirs(output_dir, exist_ok=True)

    # Save each frame to the output directory
    for i, frame in enumerate(frames):
        frame_path = os.path.join(output_dir, f"frame_{i:04d}.png")
        cv2.imwrite(frame_path, cv2.cvtColor(frame, cv2.COLOR_RGB2BGR))
        print(f"Saved frame {i} to {frame_path}")
