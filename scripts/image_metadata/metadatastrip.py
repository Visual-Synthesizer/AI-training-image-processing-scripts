"""
This script removes metadata from all PNG image files in a specified folder.
The script uses concurrent processing to speed up the task.

Functionality:
1. Prompts the user to input the path to the folder and the maximum number of workers.
2. Searches for all PNG files in the specified folder.
3. Removes metadata from each PNG file while preserving the image data.
4. Uses a ProcessPoolExecutor to process multiple images concurrently.

Usage:
    Run the script and provide the folder path and the maximum number of workers when prompted.

Example:
    python script.py
"""

import concurrent.futures
import os
from PIL import Image
import piexif

# To prevent issues with extremely large images
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
        clean_image.save(file_path, format="PNG", exif=piexif.dump({}))
        print(f"Removed metadata from {file_path}")
    except Exception as e:
        print(f"Failed to process {file_path}: {e}")

if __name__ == "__main__":
    # Get user inputs
    folder_path = input("Enter the folder path: ")
    max_workers = int(input("Enter the maximum number of workers: "))

    # List all files in the folder and filter out the PNG files
    files = os.listdir(folder_path)
    png_files = [file for file in files if file.lower().endswith(".png")]

    if not png_files:
        print("No PNG files found in the folder.")
    else:
        print(f"Processing {len(png_files)} PNG images...")

    # Process the files concurrently
    with concurrent.futures.ProcessPoolExecutor(max_workers=max_workers) as executor:
        executor.map(remove_metadata, [os.path.join(folder_path, file_name) for file_name in png_files])

    print("Processing complete.")
