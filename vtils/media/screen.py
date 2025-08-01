import numpy as np


def get_screen_dimensions(media_width: int, media_height: int, diagonal_size: float):
    """
    Calculate the screen width and height based on video resolution and screen diagonal size.

    Parameters:
        media_width (int): The width of the video in pixels.
        media_height (int): The height of the video in pixels.
        diagonal_size (float): The diagonal size of the screen in meters.

    Returns:
        tuple: A tuple containing the screen width and height in meters.
    """
    # Calculate the aspect ratio
    aspect_ratio = float(media_width) / float(media_height)

    # Calculate the screen height using the diagonal size and aspect ratio
    screen_height = diagonal_size / np.sqrt(1 + aspect_ratio**2)

    # Calculate the screen width using the aspect ratio
    screen_width = screen_height * aspect_ratio

    return screen_width, screen_height
