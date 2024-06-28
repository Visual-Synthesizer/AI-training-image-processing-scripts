"""
This script renames all image files (.png, .jpg, .jpeg) in a specified base folder and its subfolders
with a new name prefix followed by the child directory name and a sequential number. The files are sorted
by their modification time before renaming.

Functionality:
1. Prompts the user to input the path to the base folder containing the image files.
2. Prompts the user to input the new file name prefix.
3. Recursively iterates over all subfolders and files in the base folder.
4. Renames each image file with the new name prefix, the child directory name, and a sequential number,
   preserving the original file extension.
5. Prints a message for each renamed file and a final message once all files have been renamed.

Usage:
    Run the script and provide the required inputs when prompted.

Example:
    python script.py
"""

import os
import pathlib

def rename_files_in_subfolders(base_folder, new_name_prefix):
    """
    Rename all image files in the specified base folder and its subfolders with a new name prefix, child directory name, and sequential number.

    Parameters:
    - base_folder (str): The path to the base folder containing the image files.
    - new_name_prefix (str): The new prefix for the file names.

    Returns:
    None
    """
    for foldername, _, filenames in os.walk(base_folder):
        # Extract only the name of the child directory from the path
        child_directory_name = os.path.basename(foldername)
        
        # Filter out the png, jpg, and jpeg files
        image_files = [file for file in filenames if file.lower().endswith(('.png', '.jpg', '.jpeg'))]
        
        # Use pathlib to get file info and sort by modification time
        image_files_path_obj = [pathlib.Path(os.path.join(foldername, file)) for file in image_files]
        image_files_path_obj.sort(key=lambda x: x.stat().st_mtime)

        for i, file_path_obj in enumerate(image_files_path_obj, 1):
            old_file_name = file_path_obj.name
            file_extension = file_path_obj.suffix  # Get the file extension (.png, .jpg, or .jpeg)
            new_file_name = f"{new_name_prefix}_{child_directory_name}_{i:03}{file_extension}"
            new_file_path = file_path_obj.with_name(new_file_name)

            os.rename(file_path_obj, new_file_path)
            print(f"Renamed {old_file_name} to {new_file_name}")

if __name__ == "__main__":
    # Get user inputs
    folder_path = input("Enter the base folder path: ")
    new_name_prefix = input("Enter the new file name prefix: ")
    
    # Rename the files
    rename_files_in_subfolders(folder_path, new_name_prefix)
    print("Files renamed.")
