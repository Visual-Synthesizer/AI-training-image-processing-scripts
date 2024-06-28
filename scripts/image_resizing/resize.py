"""
This script resizes all image files (.png, .jpg, .jpeg) in a specified directory and its subdirectories
to a new width and height using concurrent processing for efficiency.

Functionality:
1. Prompts the user to input the path to the directory containing the image files.
2. Prompts the user to input the new width and height for the images.
3. Recursively finds all image files in the specified directory and its subdirectories.
4. Resizes each image to the specified width and height using concurrent processing.
5. Prints a message for each successfully resized image and any errors encountered.

Usage:
    Run the script and provide the required inputs when prompted.

Example:
    python script.py
"""

import os
import concurrent.futures
from PIL import Image

def resize_image(image_path, new_width, new_height):
    """
    Resize an image to the specified width and height.

    Parameters:
    - image_path (str): The path to the image file.
    - new_width (int): The new width for the image.
    - new_height (int): The new height for the image.

    Returns:
    None
    """
    try:
        img = Image.open(image_path)
        img = img.resize((new_width, new_height), Image.LANCZOS)
        img.save(image_path)
        print(f'Successfully resized image {image_path}')
    except Exception as e:
        print(f'Failed to resize image {image_path}: {e}')

def find_images(directory):
    """
    Recursively find all image files in the specified directory and its subdirectories.

    Parameters:
    - directory (str): The path to the directory to search for image files.

    Returns:
    generator: A generator yielding the paths to the image files.
    """
    for foldername, subfolders, filenames in os.walk(directory):
        for filename in filenames:
            if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
                yield os.path.join(foldername, filename)

def resize_images(directory, new_width, new_height):
    """
    Resize all image files in the specified directory and its subdirectories to the specified width and height.

    Parameters:
    - directory (str): The path to the directory containing the image files.
    - new_width (int): The new width for the images.
    - new_height (int): The new height for the images.

    Returns:
    None
    """
    images = list(find_images(directory))
    with concurrent.futures.ThreadPoolExecutor() as executor:
        for image in images:
            executor.submit(resize_image, image, new_width, new_height)

if __name__ == "__main__":
    # Get user inputs
    directory = input("Enter the directory: ")
    new_width = int(input("Enter the new width: "))
    new_height = int(input("Enter the new height: "))
    
    # Resize the images
    resize_images(directory, new_width, new_height)
