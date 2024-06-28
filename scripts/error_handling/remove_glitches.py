"""
This script processes all .txt files in a specified directory by removing single quotes and a specified phrase from the file contents.

Functionality:
1. Defines the directory where the .txt files are located.
2. Specifies the phrase to be removed from the file contents.
3. Iterates over all .txt files in the directory.
4. Reads the content of each .txt file, removes single quotes and the specified phrase, and writes the cleaned content back to the file.

Usage:
    Adjust the 'directory' and 'phrase_to_remove' variables to match your requirements.

Example:
    python script.py
"""

import os

# Define the directory where your .txt files are located
directory = '/PATH/datasets copy'

# Define the phrase to be removed
phrase_to_remove = "The tags for this image would be:"

# Iterate over all the files in the directory
for filename in os.listdir(directory):
    if filename.endswith('.txt'):
        # Construct the full file path
        file_path = os.path.join(directory, filename)
        
        # Open and read the file's content
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()

        # Remove single quotes and the specified phrase
        content = content.replace("'", "")
        content = content.replace(phrase_to_remove, "")

        # Write the cleaned content back to the file
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(content)

print("Files have been processed and cleaned.")
