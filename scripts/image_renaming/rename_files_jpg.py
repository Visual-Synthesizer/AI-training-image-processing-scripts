"""
This script renames all .jpg files in a specified folder with a new name prefix followed by a sequential number.

Functionality:
1. Prompts the user to input the path to the folder containing the .jpg files.
2. Prompts the user to input the new file name prefix.
3. Iterates over all .jpg files in the specified folder.
4. Renames each file with the new name prefix and a sequential number, preserving the .jpg extension.
5. Prints a message for each renamed file and a final message once all files have been renamed.

Usage:
    Run the script and provide the required inputs when prompted.

Example:
    python script.py
"""

import os

def rename_files(folder_path, new_name_prefix):
    """
    Rename all .jpg files in the specified folder with a new name prefix followed by a sequential number.

    Parameters:
    - folder_path (str): The path to the folder containing the .jpg files.
    - new_name_prefix (str): The new prefix for the file names.

    Returns:
    None
    """
    files = os.listdir(folder_path)
    jpg_files = [file for file in files if file.lower().endswith(".jpg")]

    for i, file_name in enumerate(jpg_files, 1):
        new_file_name = f"{new_name_prefix}_{i:03}.jpg"
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
