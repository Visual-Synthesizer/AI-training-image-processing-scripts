"""
This script rotates all .png image files in a specified folder if their width is greater than their height.
The script uses concurrent processing to speed up the task and handles large and potentially corrupted images.

Functionality:
1. Prompts the user to input the path to the folder containing the .png files.
2. Prompts the user to input the maximum number of workers for concurrent processing.
3. Recursively finds all .png files in the specified folder.
4. Rotates each image if its width is greater than its height.
5. Saves the rotated image in the original format.
6. Prints a message for each rotated image, skipped image, and any errors encountered.

Usage:
    Run the script and provide the required inputs when prompted.

Example:
    python script.py
"""

import os
import concurrent.futures
from PIL import Image
from PIL import ImageFile

# Increase the maximum allowed image size.
Image.MAX_IMAGE_PIXELS = None

# This line tells PIL to be forgiving of image files that are truncated.
ImageFile.LOAD_TRUNCATED_IMAGES = True

def rotate_image(file_path):
    """
    Rotate an image if its width is greater than its height.

    Parameters:
    - file_path (str): The path to the image file.

    Returns:
    None
    """
    try:
        image = Image.open(file_path)
        # If width > height, rotate the image
        if image.size[0] > image.size[1]:
            rotated_image = image.rotate(90, expand=True)
            rotated_image.save(file_path, format="PNG")
            print(f"Rotated {file_path}")
        else:
            print(f"Skipped {file_path} (size: {image.size[0]}x{image.size[1]})")
    except IOError:
        print(f"Failed to process {file_path}. The file might be corrupted or truncated.")

def rotate_images(folder_path, max_workers):
    """
    Rotate all .png images in the specified folder if their width is greater than their height.

    Parameters:
    - folder_path (str): The path to the folder containing the .png files.
    - max_workers (int): The maximum number of workers for concurrent processing.

    Returns:
    None
    """
    files = os.listdir(folder_path)
    png_files = [os.path.join(folder_path, file) for file in files if file.lower().endswith(".png")]

    with concurrent.futures.ProcessPoolExecutor(max_workers=max_workers) as executor:
        executor.map(rotate_image, png_files)

if __name__ == "__main__":
    # Get user inputs
    folder_path = input("Enter the folder path: ")
    max_workers = int(input("Enter the maximum number of workers: "))
    
    # Rotate the images
    rotate_images(folder_path, max_workers)
    print("Images rotated.")
