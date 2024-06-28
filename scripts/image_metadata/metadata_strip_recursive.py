"""
This script removes metadata from all image files (.png, .jpg, .jpeg) in a specified base folder and its subfolders.
The script uses concurrent processing to speed up the task.

Functionality:
1. Prompts the user to input the path to the base folder and the maximum number of workers.
2. Searches for all image files with specified extensions in the base folder and its subfolders.
3. Removes metadata from each image file while preserving the original file format.
4. Uses a ProcessPoolExecutor to process multiple images concurrently.

Usage:
    Run the script and provide the base folder path and the maximum number of workers when prompted.

Example:
    python script.py
"""

import concurrent.futures
import os
from PIL import Image
import piexif

Image.MAX_IMAGE_PIXELS = None

def remove_metadata(file_path):
    """
    Remove metadata from the image file.

    Parameters:
    - file_path (str): The path to the image file.

    Returns:
    None
    """
    try:
        image = Image.open(file_path)
        if "exif" in image.info:
            del image.info["exif"]
        clean_image = Image.new(image.mode, image.size)
        clean_image.putdata(image.getdata())
        
        # Preserve the original file format (PNG, JPG, or JPEG) when saving
        file_format = file_path.split('.')[-1].upper()
        
        clean_image.save(file_path, format=file_format, exif=piexif.dump({}))
        print(f"Removed metadata from {file_path}")
    except Exception as e:
        print(f"Failed to process {file_path}: {e}")

def find_image_files(base_folder):
    """
    Find all image files in the base folder and its subfolders.

    Parameters:
    - base_folder (str): The path to the base folder.

    Returns:
    generator: A generator yielding the paths to the image files.
    """
    for foldername, _, filenames in os.walk(base_folder):
        for filename in filenames:
            if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
                yield os.path.join(foldername, filename)

if __name__ == "__main__":
    folder_path = input("Enter the base folder path: ")
    max_workers = int(input("Enter the maximum number of workers: "))

    image_files = list(find_image_files(folder_path))

    if not image_files:
        print("No image files found in the folder.")
    else:
        print(f"Processing {len(image_files)} images...")

    with concurrent.futures.ProcessPoolExecutor(max_workers=max_workers) as executor:
        executor.map(remove_metadata, image_files)

    print("Processing complete.")
