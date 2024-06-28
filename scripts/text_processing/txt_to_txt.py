"""
This script processes a file containing multiline descriptions associated with image files,
and saves each description to a separate text file named after the image file but with a .txt extension.

Functionality:
1. Reads a file with lines formatted as 'file_number.jpg description' or continuing description lines.
2. Uses a regex pattern to identify image file names and their corresponding descriptions.
3. Collects multiline descriptions for each image file.
4. Creates a corresponding .txt file for each image file and writes the description to it.
5. Saves the .txt files in a specified output directory.

Usage:
    Ensure the input file path and the output directory are correctly specified in the script.
    Run the script to process the descriptions and save them as text files.

Example:
    python script.py
"""

import re

def create_text_files_from_multiline_descriptions(file_path, output_path):
    """
    Process a file with multiline descriptions and save each description to a corresponding text file.

    Parameters:
    - file_path (str): The path to the file containing image file names and descriptions.
    - output_path (str): The directory where the output text files will be saved.

    Returns:
    None
    """
    # This pattern matches the image file names at the start of a line and captures the number
    pattern = re.compile(r"(\d+)\.jpg")
    
    # Initialize a dictionary to store the descriptions
    descriptions = {}
    
    # Read the file
    with open(file_path, 'r') as file:
        lines = file.readlines()
    
    # Process each line
    for line in lines:
        # Check if the line matches the image file pattern
        match = pattern.match(line)
        if match:
            # Start a new entry in the dictionary
            file_number = match.group(1)
            descriptions[file_number] = line[len(match.group(0)):].strip() + "\n"
        else:
            # If it's not a new file name, it's part of the previous file's description
            descriptions[file_number] += line.strip() + "\n"
    
    # Write the descriptions to their respective new files
    for file_number, description in descriptions.items():
        new_file_name = f"{output_path}/{file_number}.txt"
        with open(new_file_name, 'w') as new_file:
            new_file.write(description)
            print(f"Created file: {new_file_name}")

if __name__ == "__main__":
    # Set the file path for V3.txt and the output path
    file_path = '/PATH/IMAGE.txt'
    output_path = '/PATH/TOFOLDER'
    
    # Call the function to create the text files
    create_text_files_from_multiline_descriptions(file_path, output_path)
