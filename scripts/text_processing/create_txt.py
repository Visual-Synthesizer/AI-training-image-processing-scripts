"""
This script takes a folder path as input and recursively searches through all the subfolders
for image files with '.jpg' or '.png' extensions. For each image found, it creates a text (.txt) file
with the same name in the same directory, containing a placeholder text related to the image file.

Functionality:
1. Prompts the user to specify the path to the folder where the search should begin.
2. Recursively searches for image files with '.jpg' or '.png' extensions in the specified folder and its subfolders.
3. For each image file found, creates a text file with the same name and writes a placeholder text into it.

Usage:
    Replace 'your_folder_path_here' with the actual folder path you want to process.

Example:
    python script.py
"""

import os

def create_text_files_for_images(folder_path):
    """
    Recursively reads file names of images (jpg or png) in the given folder path
    and creates a .txt file with the same name as the images.

    Parameters:
    - folder_path (str): The path to the folder where the search should begin.

    Returns:
    None
    """
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            if file.lower().endswith(('.jpg', '.png')):
                full_path = os.path.join(root, file)
                txt_file_path = full_path.rsplit('.', 1)[0] + '.txt'
                with open(txt_file_path, 'w') as txt_file:
                    txt_file.write(f"This is a placeholder for {file}.")

# Example usage:
# Replace 'your_folder_path_here' with the actual folder path you want to process.
folder_path = input("Enter the folder path: ")
create_text_files_for_images(folder_path)

print("Text files created for all images in the folder.")
