"""
This script prepends a specified text to all text files in a given directory.

Functionality:
1. Checks if the specified directory exists.
2. Iterates over all files in the directory.
3. For each text file, reads its content, prepends the specified text, and writes the new content back to the file.

Usage:
    Adjust the `directory_path` and `text_to_prepend` variables to specify the target directory and the text to prepend.

Example:
    directory_path = '/path/to/your/directory'
    text_to_prepend = 'Your text here, '
    prepend_text_to_files(directory_path, text_to_prepend)
"""

import os

def prepend_text_to_files(directory_path, text_to_prepend):
    """
    Prepend specified text to all text files in a given directory.

    Parameters:
        directory_path (str): The path to the directory containing the text files.
        text_to_prepend (str): The text to prepend to each file's content.
    """
    # Check if the given directory exists
    if not os.path.isdir(directory_path):
        print(f"The directory {directory_path} does not exist.")
        return

    # Iterate over all files in the given directory
    for filename in os.listdir(directory_path):
        # Construct the full file path
        file_path = os.path.join(directory_path, filename)
        # Check if the current file is a text file
        if os.path.isfile(file_path) and file_path.endswith('.txt'):
            # Read the contents of the file
            with open(file_path, 'r') as file:
                content = file.read()
            # Prepend the text to the contents
            content = text_to_prepend + content
            # Write the new content back to the file
            with open(file_path, 'w') as file:
                file.write(content)
            print(f"Prepended text to {filename}")

# Usage example:
directory_path = '/PATH/v2_token'  # Change this to your folder path
text_to_prepend = 'Faena, '
prepend_text_to_files(directory_path, text_to_prepend)
