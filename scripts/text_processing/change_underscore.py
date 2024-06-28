"""
This script renames files in a specified directory by replacing double underscores '__' 
with a single underscore '_' for files with specific extensions (.png, .txt, .npz).

Functionality:
1. Prompts the user to input the path to the directory containing the files.
2. Checks if the specified directory exists.
3. Iterates through each file in the directory.
4. For files with double underscores in their names and specific extensions (.png, .txt, .npz), 
   it renames them by replacing the double underscores with a single underscore.
5. Logs the renaming of each relevant file.

Usage:
    Run the script and provide the path to the directory when prompted.

Example:
    python script.py
"""

import os

# Ask the user to input the path to the directory
directory = input("Please enter the path to the folder: ")

# Check if the directory exists
if not os.path.isdir(directory):
    print("The specified directory does not exist. Please check the path and try again.")
else:
    # Iterate through each file in the directory
    for filename in os.listdir(directory):
        # Check if the file has a double underscore and is one of the specified file types
        if '__' in filename and filename.endswith(('.png', '.txt', '.npz')):
            new_filename = filename.replace('__', '_')
            old_file_path = os.path.join(directory, filename)
            new_file_path = os.path.join(directory, new_filename)

            # Rename the file
            os.rename(old_file_path, new_file_path)
            print(f"Renamed {filename} to {new_filename}")

    print("All relevant files have been renamed.")
