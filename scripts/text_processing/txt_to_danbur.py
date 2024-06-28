"""
This script reads a file containing image file names and their corresponding captions,
and then saves each caption to a separate text file named after the image file, but with a .txt extension.

Functionality:
1. Reads a file with lines formatted as 'file_name.jpg: caption'.
2. Skips empty lines.
3. Extracts the file name and caption from each line.
4. Creates a corresponding .txt file for each image file and writes the caption to it.
5. Saves the .txt files in a specified directory.

Usage:
    Ensure the input file path and the output directory are correctly specified in the script.
    Run the script to process the descriptions and save them as text files.

Example:
    python script.py
"""

import os

def process_and_save_descriptions(file_path):
    """
    Process a file with image file names and captions, and save each caption to a corresponding text file.

    Parameters:
    - file_path (str): The path to the file containing image file names and captions.

    Returns:
    str: A message indicating the processing result.
    """
    with open(file_path, 'r') as file:
        lines = file.readlines()

    for line in lines:
        # Skipping empty lines
        if line.strip():
            # Extract the file name and caption
            file_name, caption = line.strip().split(': ', 1)
            text_file_name = file_name.replace('.jpg', '.txt')

            # Corrected path for the new text file
            new_text_file_path = os.path.join('/PATH/', text_file_name)

            # Write the caption to the corresponding text file
            with open(new_text_file_path, 'w') as text_file:
                text_file.write(caption)
    
    return "Processing complete. Descriptions saved as text files."

if __name__ == "__main__":
    # Example usage
    dataset_file_path = '/PATH/NAME.txt'
    process_result = process_and_save_descriptions(dataset_file_path)
    print(process_result)
