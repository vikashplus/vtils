import cv2

# Load the image using OpenCV
def image_to_frame(image_path):
    """
    Converts an image file to an RGB NumPy array.

    This function reads an image from the specified file path and converts it
    from BGR to RGB format using OpenCV. If the image cannot be loaded, a
    ValueError is raised.

    Parameters:
        image_path (str): The file path to the image (WxH)

    Returns:
        np.ndarray(H,W,3): The image represented as an RGB NumPy array.

    Raises:
        ValueError: If the image cannot be loaded from the given path.
    """
    image_ndarray = cv2.imread(image_path)

    # Check if the image was loaded successfully
    if image_ndarray is None:
        raise ValueError(f"Error loading image: {image_path}")

    # Convert the image from BGR to RGB if needed
    image_ndarray = cv2.cvtColor(image_ndarray, cv2.COLOR_BGR2RGB)

    return image_ndarray
