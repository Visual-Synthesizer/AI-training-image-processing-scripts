"""
This script replaces all periods with commas in all text files within a specified directory.

Functionality:
1. Prompts the user to input the path to the directory containing the text files.
2. Checks if the specified directory exists.
3. Iterates through each text file in the directory.
4. Reads the content of each text file, replaces all periods with commas, and writes the updated content back to the file.
5. Logs the processing of each file.

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
        if filename.endswith(".txt"):  # Check if the file is a .txt file
            file_path = os.path.join(directory, filename)  # Create the full file path
            with open(file_path, 'r') as file:
                content = file.read()

            # Replace all periods with commas
            updated_content = content.replace('.', ',')

            # Write the updated content back to the file
            with open(file_path, 'w') as file:
                file.write(updated_content)

            print(f"Processed {filename}")

    print("All files have been processed.")
