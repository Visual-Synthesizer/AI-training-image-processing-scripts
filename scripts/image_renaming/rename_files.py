"""
This script renames all image files (.png, .jpg, .jpeg) in a specified folder with a new name prefix followed by a sequential number.

Functionality:
1. Prompts the user to input the path to the folder containing the image files.
2. Prompts the user to input the new file name prefix.
3. Iterates over all image files in the specified folder.
4. Renames each file with the new name prefix and a sequential number, preserving the original file extension.
5. Prints a message for each renamed file and a final message once all files have been renamed.

Usage:
    Run the script and provide the required inputs when prompted.

Example:
    python script.py
"""

import os

def rename_files(folder_path, new_name_prefix):
    """
    Rename all image files (.png, .jpg, .jpeg) in the specified folder with a new name prefix followed by a sequential number.

    Parameters:
    - folder_path (str): The path to the folder containing the image files.
    - new_name_prefix (str): The new prefix for the file names.

    Returns:
    None
    """
    files = os.listdir(folder_path)
    image_files = [file for file in files if file.lower().endswith((".png", ".jpg", ".jpeg"))]

    for i, file_name in enumerate(image_files, 1):
        file_extension = os.path.splitext(file_name)[1]
        new_file_name = f"{new_name_prefix}_{i:03}{file_extension}"
        old_file_path = os.path.join(folder_path, file_name)
        new_file_path = os.path.join(folder_path, new_file_name)

        os.rename(old_file_path, new_file_path)
        print(f"Renamed {file_name} to {new_file_name}")

if __name__ == "__main__":
    # Get user inputs
    folder_path = input("Enter the folder path: ")
    new_name_prefix = input("Enter the new file name prefix: ")
    
    # Rename the files
    rename_files(folder_path, new_name_prefix)
    print("Files renamed.")
