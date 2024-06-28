"""
This script renames all .png files in a specified folder with a new name prefix followed by a sequential number.

Functionality:
1. Prompts the user to input the path to the folder containing the .png files.
2. Prompts the user to input the new file name prefix.
3. Prompts the user to input the start number for renaming.
4. Iterates over all .png files in the specified folder.
5. Renames each file with the new name prefix and a sequential number, preserving the .png extension.
6. Prints a message for each renamed file and a final message once all files have been renamed.

Usage:
    Run the script and provide the required inputs when prompted.

Example:
    python script.py
"""

import os

def rename_files(folder_path, new_name_prefix, start_number):
    """
    Rename all .png files in the specified folder with a new name prefix followed by a sequential number.

    Parameters:
    - folder_path (str): The path to the folder containing the .png files.
    - new_name_prefix (str): The new prefix for the file names.
    - start_number (int): The starting number for the sequential numbering.

    Returns:
    None
    """
    files = os.listdir(folder_path)
    png_files = [file for file in files if file.lower().endswith(".png")]

    for i, file_name in enumerate(png_files, start=start_number):
        new_file_name = f"{new_name_prefix}_{i:03}.png"
        old_file_path = os.path.join(folder_path, file_name)
        new_file_path = os.path.join(folder_path, new_file_name)

        os.rename(old_file_path, new_file_path)
        print(f"Renamed {file_name} to {new_file_name}")

if __name__ == "__main__":
    # Get user inputs
    folder_path = input("Enter the folder path: ")
    new_name_prefix = input("Enter the new file name prefix: ")
    start_number = int(input("Enter the start number for renaming: "))
    
    # Rename the files
    rename_files(folder_path, new_name_prefix, start_number)
    print("Files renamed.")
